import flask_restful


class StopAgentCheck(flask_restful.Resource):
    def get(self, monkey_guid: int):
        if monkey_guid % 2:
            return {"stop_agent": True}
        else:
            return {"stop_agent": False}
