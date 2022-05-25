import json

from flask import request

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.server_utils.encryption import PasswordBasedStringEncryptor
from monkey_island.cc.services.config import ConfigService


class ConfigurationExport(AbstractResource):
    urls = ["/api/configuration/export"]

    @jwt_required
    def post(self):
        data = json.loads(request.data)
        should_encrypt = data["should_encrypt"]

        plaintext_config = ConfigService.get_config()

        config_export = plaintext_config
        if should_encrypt:
            password = data["password"]
            plaintext_config = json.dumps(plaintext_config)

            pb_encryptor = PasswordBasedStringEncryptor(password)
            config_export = pb_encryptor.encrypt(plaintext_config)

        return {"config_export": config_export, "encrypted": should_encrypt}
