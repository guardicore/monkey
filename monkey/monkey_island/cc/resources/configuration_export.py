from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.config import ConfigService


class ConfigurationExport(AbstractResource):
    urls = ["/api/configuration/export"]

    @jwt_required
    def post(self):
        plaintext_config = ConfigService.get_config()

        config_export = plaintext_config

        return {"config_export": config_export, "encrypted": False}
