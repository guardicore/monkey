from datetime import datetime

import flask_restful
from flask import request, make_response, jsonify

from cc.database import mongo
from cc.services.config import ConfigService
from cc.services.node import NodeService
from cc.services.report import ReportService
from cc.utils import local_ip_addresses

__author__ = 'Barak'


class Root(flask_restful.Resource):
    def get(self, action=None):
        if not action:
            action = request.args.get('action')

        if not action:
            return Root.get_server_info()
        elif action == "reset":
            return Root.reset_db()
        elif action == "killall":
            return Root.kill_all()
        else:
            return make_response(400, {'error': 'unknown action'})

    @staticmethod
    def get_server_info():
        return jsonify(ip_addresses=local_ip_addresses(), mongo=str(mongo.db),
                       completed_steps=Root.get_completed_steps())

    @staticmethod
    def reset_db():
        [mongo.db[x].drop() for x in ['config', 'monkey', 'telemetry', 'node', 'edge', 'report']]
        ConfigService.init_config()
        return jsonify(status='OK')

    @staticmethod
    def kill_all():
        mongo.db.monkey.update({'dead': False}, {'$set': {'config.alive': False, 'modifytime': datetime.now()}},
                               upsert=False,
                               multi=True)
        return jsonify(status='OK')

    @staticmethod
    def get_completed_steps():
        is_any_exists = NodeService.is_any_monkey_exists()
        infection_done = NodeService.is_monkey_finished_running()
        report_done = ReportService.is_report_generated()
        return dict(run_server=True, run_monkey=is_any_exists, infection_done=infection_done, report_done=report_done)
