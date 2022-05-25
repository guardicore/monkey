from monkey_island.cc.database import mongo
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.services.config import ConfigService


class PropagationCredentials(AbstractResource):
    urls = ["/api/propagation-credentials/<string:guid>"]

    def get(self, guid: str):
        monkey_json = mongo.db.monkey.find_one_or_404({"guid": guid})
        ConfigService.decrypt_flat_config(monkey_json["config"])

        propagation_credentials = ConfigService.get_config_propagation_credentials_from_flat_config(
            monkey_json["config"]
        )

        return {"propagation_credentials": propagation_credentials}
