from monkey_island.cc.flask_utils import FlaskDIWrapper

from .agent_logs import AgentLogs
from .island_log import IslandLog


def register_resources(di_container: FlaskDIWrapper):
    di_container.add_resource(AgentLogs)
    di_container.add_resource(IslandLog)
