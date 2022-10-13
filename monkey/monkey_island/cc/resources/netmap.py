from monkey_island.cc.repository import IMachineRepository, INodeRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.netmap.net_edge import NetEdgeService
from monkey_island.cc.services.netmap.net_node import NetNodeService


class NetMap(AbstractResource):
    urls = ["/api/netmap"]

    def __init__(self, machine_repository: IMachineRepository, node_repository: INodeRepository):
        self.net_node_service = NetNodeService(machine_repository, node_repository)

    @jwt_required
    def get(self, **kw):
        net_nodes = self.net_node_service.get_all_net_nodes()
        net_edges = NetEdgeService.get_all_net_edges()

        return {"nodes": net_nodes, "edges": net_edges}
