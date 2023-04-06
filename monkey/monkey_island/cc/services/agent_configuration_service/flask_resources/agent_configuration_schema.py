from http import HTTPStatus

from flask_security import auth_token_required, roles_accepted

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentConfigurationService


class AgentConfigurationSchema(AbstractResource):
    urls = ["/api/agent-configuration-schema"]

    def __init__(self, agent_configuration_service: IAgentConfigurationService):
        self._agent_configuration_service = agent_configuration_service

    @auth_token_required
    @roles_accepted(AccountRole.AGENT.name, AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        schema = self._agent_configuration_service.get_schema()
        return schema, HTTPStatus.OK
