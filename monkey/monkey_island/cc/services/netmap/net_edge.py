from bson import ObjectId

from monkey_island.cc.models import Monkey
from monkey_island.cc.services.edge.displayed_edge import DisplayedEdgeService
from monkey_island.cc.services.edge.edge import EdgeService
from monkey_island.cc.services.node import NodeService


class NetEdgeService:

    @staticmethod
    def get_all_net_edges():
        edges = NetEdgeService._get_standard_net_edges()
        if NodeService.get_monkey_island_monkey() is None:
            edges += NetEdgeService._get_uninfected_island_net_edges()
        else:
            monkey_island_monkey = NodeService.get_monkey_island_monkey()
            edges += NetEdgeService._get_infected_island_net_edges(monkey_island_monkey)
        return edges

    @staticmethod
    def _get_standard_net_edges():
        return [DisplayedEdgeService.edge_to_net_edge(x) for x in EdgeService.get_all_edges()]

    @staticmethod
    def _get_uninfected_island_net_edges():
        edges = []
        monkey_ids = [x.id for x in Monkey.objects() if "tunnel" not in x]
        count = 0
        for monkey_id in monkey_ids:
            count += 1
            # generating fake ID, because front end requires unique ID's for each edge. Collision improbable
            fake_id = ObjectId(hex(count)[2:].zfill(24))
            island_id = ObjectId("000000000000000000000000")
            monkey_label = NodeService.get_label_for_endpoint(monkey_id)
            island_label = NodeService.get_label_for_endpoint(island_id)
            island_pseudo_edge = DisplayedEdgeService.generate_pseudo_edge(edge_id=fake_id,
                                                                           src_node_id=monkey_id,
                                                                           dst_node_id=island_id,
                                                                           src_label=monkey_label,
                                                                           dst_label=island_label)
            edges.append(island_pseudo_edge)
        return edges

    @staticmethod
    def _get_infected_island_net_edges(monkey_island_monkey):
        existing_ids = [x.src_node_id for x
                        in EdgeService.get_by_dst_node(dst_node_id=monkey_island_monkey["_id"])]
        monkey_ids = [x.id for x in Monkey.objects()
                      if ("tunnel" not in x) and
                      (x.id not in existing_ids) and
                      (x.id != monkey_island_monkey["_id"])]
        edges = []

        count = 0
        for monkey_id in monkey_ids:
            count += 1
            # generating fake ID, because front end requires unique ID's for each edge. Collision improbable
            fake_id = ObjectId(hex(count)[2:].zfill(24))
            src_label = NodeService.get_label_for_endpoint(monkey_id)
            dst_label = NodeService.get_label_for_endpoint(monkey_island_monkey["_id"])
            edge = DisplayedEdgeService.generate_pseudo_edge(edge_id=fake_id,
                                                             src_node_id=monkey_id,
                                                             dst_node_id=monkey_island_monkey["_id"],
                                                             src_label=src_label,
                                                             dst_label=dst_label)
            edges.append(edge)

        return edges
