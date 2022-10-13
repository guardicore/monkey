from typing import List

from monkey_island.cc.database import mongo
from monkey_island.cc.repository import IMachineRepository, INodeRepository
from monkey_island.cc.services.netmap.utils import fixup_group_and_os
from monkey_island.cc.services.node import NodeService


class NetNodeService:
    def __init__(self, machine_repository: IMachineRepository, node_repository: INodeRepository):
        self.machine_repository = machine_repository
        self.node_repository = node_repository

    def get_all_net_nodes(self):
        legacy_agents = self._get_monkey_net_nodes()
        legacy_nodes = self._get_standard_net_nodes()
        if NodeService.get_monkey_island_monkey() is None:
            monkey_island = [NodeService.get_monkey_island_pseudo_net_node()]
        else:
            monkey_island = []

        return legacy_agents + legacy_nodes + monkey_island

    def _get_monkey_net_nodes(self):
        formatted_nodes = []
        for legacy_agent in mongo.db.monkey.find({}):
            formatted_node = NodeService.monkey_to_net_node(legacy_agent)
            machine = self.machine_repository.get_machines_by_ip(legacy_agent["ip_addresses"][0])[0]
            formatted_nodes.append(fixup_group_and_os(formatted_node, machine))
        return formatted_nodes

    def _get_standard_net_nodes(self) -> List[dict]:
        formatted_nodes = []
        for node in mongo.db.node.find({}):
            formatted_node = NodeService.node_to_net_node(node)
            machine = self.machine_repository.get_machines_by_ip(node["ip_addresses"][0])[0]
            formatted_nodes.append(fixup_group_and_os(formatted_node, machine))
        return formatted_nodes
