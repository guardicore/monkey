from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.services.config import ConfigService


class PropagationCredentials(AbstractResource):
    urls = ["/api/propagation-credentials"]

    def get(self):
        config = ConfigService.get_flat_config(should_decrypt=True)

        propagation_credentials = ConfigService.get_config_propagation_credentials_from_flat_config(
            config
        )

        return {"propagation_credentials": propagation_credentials}
