from monkey_island.cc.flask_utils import FlaskDIWrapper

from .agent_configuration import AgentConfiguration
from .agent_configuration_schema import AgentConfigurationSchema


def register_resources(api: FlaskDIWrapper):
    api.add_resource(AgentConfiguration)
    api.add_resource(AgentConfigurationSchema)
