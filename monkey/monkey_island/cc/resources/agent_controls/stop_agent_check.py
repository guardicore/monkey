from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.services.infection_lifecycle import should_agent_die

class StopAgentCheck(AbstractResource):
    # API Spec: Rename to AgentStopStatus or something
    urls = ["/api/monkey-control/needs-to-stop/<int:monkey_guid>"]

    def get(self, monkey_guid: int):
        return {"stop_agent": should_agent_die(monkey_guid)}
