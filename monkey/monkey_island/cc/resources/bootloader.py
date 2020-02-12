import json

import flask_restful
from flask import request, make_response

from monkey_island.cc.database import mongo
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
        data = json.loads(request.data.decode().replace("\n", ""))

        # Remove local ips
        local_addr = [i for i in data["ips"] if i.startswith("127")]
        if local_addr:
            data["ips"].remove(local_addr[0])

        # Clean up os info
        data['os_version'] = data['os_version'].split(" ")[0]

        mongo.db.bootloader_telems.insert(data)
        node_id = NodeService.get_or_create_node_from_bootloader_telem(data)


        return make_response({"status": "OK"}, 200)
