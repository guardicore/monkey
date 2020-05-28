from copy import deepcopy

from bson import ObjectId

from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.edge import Edge
from monkey_island.cc.services.edge.edge import EdgeService

__author__ = "itay.mizeretz"


class DisplayedEdgeService:

    @staticmethod
    def get_displayed_edges_by_dst(dst_id, for_report=False):
        edges = Edge.objects(dst_node_id=ObjectId(dst_id))
        return [DisplayedEdgeService.edge_to_displayed_edge(edge, for_report) for edge in edges]

    @staticmethod
    def get_displayed_edge_by_id(edge_id, for_report=False):
        edge = Edge.objects.get(id=edge_id)
        displayed_edge = DisplayedEdgeService.edge_to_displayed_edge(edge, for_report)
        return displayed_edge

    @staticmethod
    def edge_to_displayed_edge(edge: Edge, for_report=False):
        services = []
        os = {}

        if len(edge.scans) > 0:
            services = DisplayedEdgeService.services_to_displayed_services(edge.scans[-1]["data"]["services"],
                                                                           for_report)
            os = edge.scans[-1]["data"]["os"]

        displayed_edge = DisplayedEdgeService.edge_to_net_edge(edge)

        displayed_edge["ip_address"] = edge['ip_address']
        displayed_edge["services"] = services
        displayed_edge["os"] = os
        # we need to deepcopy all mutable edge properties, because weak-reference link is made otherwise,
        # which is destroyed after method is exited and causes an error later.
        displayed_edge["exploits"] = deepcopy(edge['exploits'])
        displayed_edge["_label"] = EdgeService.get_edge_label(displayed_edge)
        return displayed_edge

    @staticmethod
    def generate_pseudo_edge(edge_id, src_node_id, dst_node_id, src_label, dst_label):
        edge = \
            {
                "id": edge_id,
                "from": src_node_id,
                "to": dst_node_id,
                "group": "island",
                "src_label": src_label,
                "dst_label": dst_label
            }
        edge["_label"] = EdgeService.get_edge_label(edge)
        return edge

    @staticmethod
    def get_infected_monkey_island_pseudo_edges(monkey_island_monkey):
        existing_ids = [x.src_node_id for x in Edge.objects(dst_node_id=monkey_island_monkey["_id"])]
        monkey_ids = [x["_id"] for x in mongo.db.monkey.find({})
                      if ("tunnel" not in x) and
                      (x["_id"] not in existing_ids) and
                      (x["_id"] != monkey_island_monkey["_id"])]
        edges = []

        # We're using fake ids because the frontend graph module requires unique ids.
        # Collision with real id is improbable.
        count = 0
        for monkey_id in monkey_ids:
            count += 1
            edges.append(DisplayedEdgeService.generate_pseudo_edge(
                ObjectId(hex(count)[2:].zfill(24)), monkey_id, monkey_island_monkey["_id"]))

        return edges

    @staticmethod
    def services_to_displayed_services(services, for_report=False):
        if for_report:
            return [x for x in services]
        else:
            return [x + ": " + (services[x]['name'] if 'name' in services[x] else 'unknown') for x in services]

    @staticmethod
    def edge_to_net_edge(edge: Edge):
        return \
            {
                "id": edge.id,
                "from": edge.src_node_id,
                "to": edge.dst_node_id,
                "group": EdgeService.get_edge_group(edge),
                "src_label": edge.src_label,
                "dst_label": edge.dst_label
            }


RIGHT_ARROW = "\u2192"
