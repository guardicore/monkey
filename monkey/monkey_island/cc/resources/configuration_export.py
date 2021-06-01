import json

import flask_restful
from flask import request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.utils.config_encryption import encrypt_config


class ConfigurationExport(flask_restful.Resource):
    @jwt_required
    def get(self):
        return {"to_export": self.config_to_return, "is_plaintext": self.is_plaintext}

    @jwt_required
    def post(self):
        data = json.loads(request.data)
        should_encrypt = data["should_encrypt"]

        plaintext_config = ConfigService.get_config()

        self.config_to_return = plaintext_config
        self.is_plaintext = True
        if should_encrypt:
            password = data["password"]
            self.config_to_return = encrypt_config(plaintext_config, password)
            self.is_plaintext = False

        return self.get()
