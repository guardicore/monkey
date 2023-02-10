from http import HTTPStatus

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.services import AgentConfigurationSchemaService


class AgentConfigurationSchema(AbstractResource):
    urls = ["/api/agent-configuration-schema"]

    def __init__(self, config_schema_service: AgentConfigurationSchemaService):
        self._config_schema_service = config_schema_service

    # Used by the agent. Can't secure.
    def get(self):
        schema = self._config_schema_service.get_schema()
        return schema, HTTPStatus.OK
