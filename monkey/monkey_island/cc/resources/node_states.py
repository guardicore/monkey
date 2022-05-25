from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.utils.node_states import NodeStates as NodeStateList


class NodeStates(AbstractResource):
    urls = ["/api/netmap/node-states"]

    @jwt_required
    def get(self):
        return {"node_states": [state.value for state in NodeStateList]}
