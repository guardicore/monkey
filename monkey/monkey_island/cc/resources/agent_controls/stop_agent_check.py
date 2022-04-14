import flask_restful

from monkey_island.cc.services.infection_lifecycle import should_agent_die


class StopAgentCheck(flask_restful.Resource):
    def get(self, monkey_guid: int):
        return {"stop_agent": should_agent_die(monkey_guid)}
