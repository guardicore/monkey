import flask_restful

from monkey_island.cc.resources.i_resource import IResource
from monkey_island.cc.services.infection_lifecycle import should_agent_die


class StopAgentCheck(flask_restful.Resource, IResource):
    urls = ["/api/monkey-control/needs-to-stop/<int:monkey_guid>"]

    def get(self, monkey_guid: int):
        return {"stop_agent": should_agent_die(monkey_guid)}
