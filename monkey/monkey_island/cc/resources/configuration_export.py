import json
import os

import flask_restful
from flask import jsonify, request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.utils.file_handler import encrypt_file_with_password


class ConfigurationExport(flask_restful.Resource):
    @jwt_required
    def get(self):
        return jsonify(
            config_encrypted=self.file_encryption_successful,
            plaintext_removed=self.plaintext_file_removal_successful,
        )

    @jwt_required
    def post(self):
        data = json.loads(request.data)

        config = ConfigService.get_config()

        config_filename = "monkey.conf"
        plaintext_config_path = os.path.join(DEFAULT_DATA_DIR, config_filename)
        with open(plaintext_config_path) as file:
            json.dump(config, file)

        self.file_encryption_successful = self.plaintext_file_removal_successful = False
        if "password" in data:
            encrypted_config_path = os.path.join(DEFAULT_DATA_DIR, f"encrypted_{config_filename}")
            (
                self.file_encryption_successful,
                self.plaintext_file_removal_successful,
            ) = encrypt_file_with_password(
                plaintext_config_path, encrypted_config_path, data["password"]
            )

        return self.get()
