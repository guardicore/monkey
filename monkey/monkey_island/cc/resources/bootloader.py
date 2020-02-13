import json
from typing import Dict

import flask_restful
from flask import request, make_response

from monkey_island.cc.services.bootloader import BootloaderService


class Bootloader(flask_restful.Resource):

    # Used by monkey. can't secure.
    def post(self, **kw):
        data = Bootloader.parse_bootloader_request(request.data)
        resp = BootloaderService.parse_bootloader_data(data)
        return make_response({"status": "OK"}, 200)

    @staticmethod
    def parse_bootloader_request(request_data: bytes) -> Dict[str, str]:
        parsed_data = json.loads(request_data.decode().replace("\n", "")
                                                         .replace("NAME=\"", "")
                                                         .replace("\"\"", "\""))
        return parsed_data
