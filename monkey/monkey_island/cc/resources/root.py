from datetime import datetime
import logging
import threading

import flask_restful
from flask import request, make_response, jsonify

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.database import mongo
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.reporting.report import ReportService
from monkey_island.cc.services.attack.attack_report import AttackReportService
from monkey_island.cc.utils import local_ip_addresses
from monkey_island.cc.services.database import Database

__author__ = 'Barak'

logger = logging.getLogger(__name__)


class Root(flask_restful.Resource):
    def __init__(self):
        self.report_generating_lock = threading.Event()

    def get(self, action=None):
        if not action:
            action = request.args.get('action')

        if not action:
            return self.get_server_info()
        elif action == "reset":
            return jwt_required()(Database.reset_db)()
        elif action == "killall":
            return Root.kill_all()
        elif action == "is-up":
            return {'is-up': True}
        else:
            return make_response(400, {'error': 'unknown action'})

    @jwt_required()
    def get_server_info(self):
        return jsonify(ip_addresses=local_ip_addresses(), mongo=str(mongo.db),
                       completed_steps=self.get_completed_steps())

    @staticmethod
    @jwt_required()
    def kill_all():
        mongo.db.monkey.update({'dead': False}, {'$set': {'config.alive': False, 'modifytime': datetime.now()}},
                               upsert=False,
                               multi=True)
        logger.info('Kill all monkeys was called')
        return jsonify(status='OK')

    @jwt_required()
    def get_completed_steps(self):
        is_any_exists = NodeService.is_any_monkey_exists()
        infection_done = NodeService.is_monkey_finished_running()

        if infection_done:
            if self.should_generate_report():
                self.generate_report()
            report_done = ReportService.is_report_generated()
        else:  # Infection is not done
            report_done = False

        return dict(
            run_server=True,
            run_monkey=is_any_exists,
            infection_done=infection_done,
            report_done=report_done)

    def generate_report(self):
        # Set the event - enter the critical section
        self.report_generating_lock.set()
        # Not using the return value, as the get_report function also saves the report in the DB for later.
        _ = ReportService.get_report()
        _ = AttackReportService.get_latest_report()
        # Clear the event - exit the critical section
        self.report_generating_lock.clear()

    def should_generate_report(self):
        # If the lock is not set, that means no one is generating a report right now.
        is_any_thread_generating_a_report_right_now = not self.report_generating_lock.is_set()
        return is_any_thread_generating_a_report_right_now and not ReportService.is_latest_report_exists()
