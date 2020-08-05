import logging
import threading

import flask_restful
from flask import jsonify, make_response, request

from monkey_island.cc.database import mongo
from monkey_island.cc.network_utils import local_ip_addresses
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.database import Database
from monkey_island.cc.services.infection_lifecycle import InfectionLifecycle

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
            return jwt_required(Database.reset_db)()
        elif action == "killall":
            return jwt_required(InfectionLifecycle.kill_all)()
        elif action == "is-up":
            return {'is-up': True}
        else:
            return make_response(400, {'error': 'unknown action'})

    @jwt_required
    def get_server_info(self):
        return jsonify(
            ip_addresses=local_ip_addresses(),
            mongo=str(mongo.db),
            completed_steps=InfectionLifecycle.get_completed_steps())
