import flask_restful
from flask import request

from monkey_island.cc.services.remote_port_check import check_tcp_port


class RemotePortCheck(flask_restful.Resource):

    # Used by monkey. can't secure.
    def get(self, port):
        if port and check_tcp_port(request.remote_addr, port):
            return {"status": "port_visible"}
        else:
            return {"status": "port_invisible"}
