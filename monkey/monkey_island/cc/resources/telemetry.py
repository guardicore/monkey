import json
import logging
from datetime import datetime

import dateutil
from flask import request

from monkey_island.cc.database import mongo
from monkey_island.cc.models.monkey import Monkey
from monkey_island.cc.models.telemetries import get_telemetry_by_query
from monkey_island.cc.repository import IAgentConfigurationRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.telemetry.processing.processing import process_telemetry

logger = logging.getLogger(__name__)


class Telemetry(AbstractResource):
    # API Spec: Resource name should be plural
    urls = ["/api/telemetry", "/api/telemetry/<string:monkey_guid>"]

    def __init__(self, agent_configuration_repository: IAgentConfigurationRepository):
        self._agent_configuration_repository = agent_configuration_repository

    @jwt_required
    def get(self, **kw):
        monkey_guid = request.args.get("monkey_guid")
        telem_category = request.args.get("telem_category")
        timestamp = request.args.get("timestamp")
        if "null" == timestamp:  # special case to avoid ugly JS code...
            timestamp = None

        result = {"timestamp": datetime.now().isoformat()}
        find_filter = {}

        if monkey_guid:
            find_filter["monkey_guid"] = {"$eq": monkey_guid}
        if telem_category:
            find_filter["telem_category"] = {"$eq": telem_category}
        if timestamp:
            find_filter["timestamp"] = {"$gt": dateutil.parser.parse(timestamp)}

        result["objects"] = self.telemetry_to_displayed_telemetry(
            get_telemetry_by_query(query=find_filter)
        )
        return result

    # Used by monkey. can't secure.
    def post(self):
        telemetry_json = json.loads(request.data)
        telemetry_json["data"] = json.loads(telemetry_json["data"])
        telemetry_json["timestamp"] = datetime.now()

        # Monkey communicated, so it's alive. Update the TTL.
        Monkey.get_single_monkey_by_guid(telemetry_json["monkey_guid"]).renew_ttl()

        monkey = NodeService.get_monkey_by_guid(telemetry_json["monkey_guid"])
        NodeService.update_monkey_modify_time(monkey["_id"])

        agent_configuration = self._agent_configuration_repository.get_configuration()
        process_telemetry(telemetry_json, agent_configuration)

        # API Spec: RESTful way is to return an identifier of the updated/newly created resource
        return {}, 201

    @staticmethod
    def telemetry_to_displayed_telemetry(telemetry):
        monkey_guid_dict = {}
        monkeys = mongo.db.monkey.find({})
        for monkey in monkeys:
            monkey_guid_dict[monkey["guid"]] = NodeService.get_monkey_label(monkey)

        objects = []
        for x in telemetry:
            telem_monkey_guid = x.pop("monkey_guid")
            monkey_label = monkey_guid_dict.get(telem_monkey_guid)
            if monkey_label is None:
                monkey_label = telem_monkey_guid
            x["monkey"] = monkey_label
            objects.append(x)

        return objects
