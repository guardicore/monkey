from datetime import datetime

from flask import request, make_response, jsonify
import flask_restful

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
            return jsonify(ip_addresses=local_ip_addresses(), mongo=str(mongo.db), completed_steps=self.get_completed_steps())

        elif action == "reset":
            mongo.db.config.drop()
            mongo.db.monkey.drop()
            mongo.db.telemetry.drop()
            mongo.db.node.drop()
            mongo.db.edge.drop()
            mongo.db.report.drop()
            ConfigService.init_config()
            return jsonify(status='OK')
        elif action == "killall":
            mongo.db.monkey.update({'dead': False}, {'$set': {'config.alive': False, 'modifytime': datetime.now()}}, upsert=False,
                                   multi=True)
            return jsonify(status='OK')
        else:
            return make_response(400, {'error': 'unknown action'})

    def get_completed_steps(self):
        is_any_exists = NodeService.is_any_monkey_exists()
        infection_done = NodeService.is_monkey_finished_running()
        report_done = ReportService.is_report_generated()
        return dict(run_server=True, run_monkey=is_any_exists, infection_done=infection_done, report_done=report_done)
