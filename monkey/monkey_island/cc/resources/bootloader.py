import flask_restful
from flask import request, make_response

from monkey_island.cc.services.node import NodeService

WINDOWS_VERSIONS = {
    "5.0": "Windows 2000",
    "5.1": "Windows XP",
    "5.2": "Windows XP/server 2003",
    "6.0": "Windows Vista/server 2008",
    "6.1": "Windows 7/server 2008R2",
    "6.2": "Windows 8/server 2012",
    "6.3": "Windows 8.1/server 2012R2",
    "10.0": "Windows 10/server 2016-2019"
}


class Bootloader(flask_restful.Resource):

    # Used by monkey. can't secure.
    def post(self, **kw):
        os_version = request.data.decode().split(" ")
        if (os_version[0][0] == "W"):
            os_type = "windows"
            os_version = os_version[1:]

        return make_response({"status": "OK"}, 200)
