from monkey_island.cc.database import mongo
from monkey_island.cc.services.node import NodeService


class NetNodeService:

    @staticmethod
    def get_all_net_nodes():
        monkeys = NetNodeService._get_monkey_net_nodes()
        nodes = NetNodeService._get_standard_net_nodes()
        if NodeService.get_monkey_island_monkey() is None:
            monkey_island = [NodeService.get_monkey_island_pseudo_net_node()]
        else:
            monkey_island = []
        return monkeys + nodes + monkey_island

    @staticmethod
    def _get_monkey_net_nodes():
        return [NodeService.monkey_to_net_node(x) for x in mongo.db.monkey.find({})]

    @staticmethod
    def _get_standard_net_nodes():
        return [NodeService.node_to_net_node(x) for x in mongo.db.node.find({})]
