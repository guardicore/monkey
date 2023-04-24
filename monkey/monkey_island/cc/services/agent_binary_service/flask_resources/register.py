from monkey_island.cc.flask_utils import FlaskDIWrapper

from .agent_binaries import AgentBinaries


def register_resources(api: FlaskDIWrapper):
    api.add_resource(AgentBinaries)
