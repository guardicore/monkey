from copy import deepcopy

from bson import ObjectId

from monkey_island.cc.services.edge.edge import EdgeService


class DisplayedEdgeService:
    @staticmethod
    def get_displayed_edges_by_dst(dst_id: str, for_report=False):
        edges = EdgeService.get_by_dst_node(dst_node_id=ObjectId(dst_id))
        return [DisplayedEdgeService.edge_to_displayed_edge(edge, for_report) for edge in edges]

    @staticmethod
    def get_displayed_edge_by_id(edge_id: str, for_report=False):
        edge = EdgeService.get_edge_by_id(ObjectId(edge_id))
        displayed_edge = DisplayedEdgeService.edge_to_displayed_edge(edge, for_report)
        return displayed_edge

    @staticmethod
    def edge_to_displayed_edge(edge: EdgeService, for_report=False):
        services = []
        os = {}

        if len(edge.scans) > 0:
            services = DisplayedEdgeService.services_to_displayed_services(
                edge.scans[-1]["data"]["services"], for_report
            )
            os = edge.scans[-1]["data"]["os"]

        displayed_edge = DisplayedEdgeService.edge_to_net_edge(edge)

        displayed_edge["ip_address"] = edge.ip_address
        displayed_edge["services"] = services
        displayed_edge["os"] = os
        # we need to deepcopy all mutable edge properties, because weak-reference link is made
        # otherwise, which is destroyed after method is exited and causes an error later.
        displayed_edge["exploits"] = deepcopy(edge.exploits)
        displayed_edge["_label"] = edge.get_label()
        return displayed_edge

    @staticmethod
    def services_to_displayed_services(services, for_report=False):
        if for_report:
            return [x for x in services]
        else:
            return [
                x + ": " + (services[x]["name"] if "name" in services[x] else "unknown")
                for x in services
            ]

    @staticmethod
    def edge_to_net_edge(edge: EdgeService):
        return {
            "id": edge.id,
            "from": edge.src_node_id,
            "to": edge.dst_node_id,
            "group": edge.get_group(),
            "src_label": edge.src_label,
            "dst_label": edge.dst_label,
        }


RIGHT_ARROW = "\u2192"
