from flask import request

from monkey_island.cc.repository import IMachineRepository, INodeRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.netmap.utils import fixup_group_and_os
from monkey_island.cc.services.node import NodeService


class Node(AbstractResource):
    urls = ["/api/netmap/node"]

    def __init__(self, node_repository: INodeRepository, machine_repository: IMachineRepository):
        self.node_repository = node_repository
        self.machine_repository = machine_repository

    @jwt_required
    def get(self):
        node_id = request.args.get("id")
        if node_id:
            legacy_node = NodeService.get_displayed_node_by_id(node_id)
            machine = self.machine_repository.get_machines_by_ip(legacy_node["ip_addresses"][0])[0]
            return fixup_group_and_os(legacy_node, machine)
        else:
            return list(self.node_repository.get_nodes())
