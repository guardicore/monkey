from http import HTTPStatus

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.services import IAgentConfigurationService


class AgentConfigurationSchema(AbstractResource):
    urls = ["/api/agent-configuration-schema"]

    def __init__(self, agent_configuration_service: IAgentConfigurationService):
        self._agent_configuration_service = agent_configuration_service

    # Used by the agent. Can't secure.
    def get(self):
        schema = self._agent_configuration_service.get_schema()
        return schema, HTTPStatus.OK
