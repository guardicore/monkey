from monkey_island.cc.flask_utils import FlaskDIWrapper

from .agent_binaries import AgentBinaries
from .agent_binaries_masque import AgentBinariesMasque


def register_resources(api: FlaskDIWrapper):
    api.add_resource(AgentBinaries)
    api.add_resource(AgentBinariesMasque)
