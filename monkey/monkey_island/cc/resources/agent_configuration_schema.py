from http import HTTPStatus

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services import ConfigSchemaService


class AgentConfigurationSchema(AbstractResource):
    urls = ["/api/agent-configuration-schema"]

    def __init__(self, config_schema_service: ConfigSchemaService):
        self._config_schema_service = config_schema_service

    @jwt_required
    def get(self):
        try:
            schema = self._config_schema_service.get_schema()
            return schema, HTTPStatus.OK
        except RuntimeError as err:
            return {"error": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR
