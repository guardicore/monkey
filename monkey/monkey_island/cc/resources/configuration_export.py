import json

import flask_restful
from flask import jsonify, request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.utils.config_encryption import encrypt_config


class ConfigurationExport(flask_restful.Resource):
    @jwt_required
    def get(self):
        return jsonify(encrypted_config=self.encrypted_config)

    @jwt_required
    def post(self):
        password = json.loads(request.data)["password"]
        plaintext_config = ConfigService.get_config()

        self.encrypted_config = encrypt_config(plaintext_config, password)

        return self.get()
