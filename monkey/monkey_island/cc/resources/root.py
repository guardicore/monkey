import logging
import threading
from datetime import datetime

import flask_restful
from flask import request, make_response, jsonify

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.database import mongo
from monkey_island.cc.services.database import Database
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.reporting.report import ReportService
from monkey_island.cc.services.reporting.report_generation_synchronisation import is_report_being_generated, \
    safe_generate_reports
from monkey_island.cc.utils import local_ip_addresses

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
        return jsonify(
            ip_addresses=local_ip_addresses(),
            mongo=str(mongo.db),
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
            # Checking is_report_being_generated here, because we don't want to wait to generate a report; rather,
            # we want to skip and reply.
            if not is_report_being_generated() and not ReportService.is_latest_report_exists():
                safe_generate_reports()
            report_done = ReportService.is_report_generated()
        else:  # Infection is not done
            report_done = False

        return dict(
            run_server=True,
            run_monkey=is_any_exists,
            infection_done=infection_done,
            report_done=report_done)
