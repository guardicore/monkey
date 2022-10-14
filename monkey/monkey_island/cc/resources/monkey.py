import json
from datetime import datetime

from flask import request

from monkey_island.cc.database import mongo
from monkey_island.cc.models.monkey_ttl import create_monkey_ttl_document
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.utils.semaphores import agent_killing_mutex
from monkey_island.cc.server_utils.consts import DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS
from monkey_island.cc.services.edge.edge import EdgeService
from monkey_island.cc.services.node import NodeService

# TODO: separate logic from interface


class Monkey(AbstractResource):
    # API Spec: Resource name should be plural
    urls = [
        "/api/agent",
        "/api/agent/<string:guid>",
    ]

    # Used by monkey. can't secure.
    # Called on monkey wakeup to initialize local configuration
    def post(self, **kw):

        # TODO: Why is it the registration of an agent coupled to exploit telemetry? It's hard to
        #       understand why an agent registering itself should be so complicated. Is it because
        #       agent state (dead) and config are conflated? Figure out why this thing is so
        #       complicated. Then simplify it.
        with agent_killing_mutex:
            monkey_json = json.loads(request.data)
            monkey_json["dead"] = False

            monkey_json["modifytime"] = datetime.now()

            # if new monkey telem, change config according to "new monkeys" config.
            db_monkey = mongo.db.monkey.find_one({"guid": monkey_json["guid"]})

            # try to find new monkey parent
            parent = monkey_json.get("parent")
            parent_to_add = (monkey_json.get("guid"), None)  # default values in case of manual run
            if parent and parent != monkey_json.get("guid"):  # current parent is known
                parent_to_add = (parent, None)

            if not db_monkey:
                monkey_json["parent"] = [parent_to_add]
            else:
                monkey_json["parent"] = db_monkey.get("parent") + [parent_to_add]

            tunnel_host_ip = None
            if "tunnel" in monkey_json:
                tunnel_host_ip = monkey_json["tunnel"].split(":")[-2].replace("//", "")
                monkey_json.pop("tunnel")

            ttl = create_monkey_ttl_document(DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS)
            monkey_json["ttl_ref"] = ttl.id

            mongo.db.monkey.update(
                {"guid": monkey_json["guid"]}, {"$set": monkey_json}, upsert=True
            )

            # Merge existing scanned node with new monkey

            new_monkey_id = mongo.db.monkey.find_one({"guid": monkey_json["guid"]})["_id"]

            if tunnel_host_ip is not None:
                NodeService.set_monkey_tunnel(new_monkey_id, tunnel_host_ip)

            existing_node = mongo.db.node.find_one(
                {"ip_addresses": {"$in": monkey_json["ip_addresses"]}}
            )

            if existing_node:
                node_id = existing_node["_id"]
                EdgeService.update_all_dst_nodes(
                    old_dst_node_id=node_id, new_dst_node_id=new_monkey_id
                )
                mongo.db.node.remove({"_id": node_id})

            return {"id": new_monkey_id}
