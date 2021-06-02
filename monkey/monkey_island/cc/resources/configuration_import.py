import json
import logging
from dataclasses import dataclass

import flask_restful
from flask import request

from common.utils.exceptions import (
    InvalidConfigurationError,
    InvalidCredentialsError,
    NoCredentialsError,
)
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.utils.config_encryption import decrypt_config


@dataclass
class ResponseContents:
    import_status: str = "imported"
    message: str = ""
    status_code: int = 200

    def form_response(self):
        return self.__dict__, self.status_code


logger = logging.getLogger(__name__)


class ConfigurationImport(flask_restful.Resource):
    SUCCESS = False

    @jwt_required
    def post(self):
        request_contents = json.loads(request.data)
        try:
            decrypt_config(request_contents["config"], request_contents["password"])
            ConfigurationImport.import_config(request_contents["config"])
            return ResponseContents().form_response()
        except InvalidCredentialsError:
            return ResponseContents(
                import_status="wrong_password", message="Wrong password supplied", status_code=403
            ).form_response()
        except InvalidConfigurationError:
            return ResponseContents(
                import_status="invalid_configuration",
                message="Invalid configuration supplied. "
                "Maybe the format is outdated or the file is corrupted.",
                status_code=400,
            ).form_response()
        except NoCredentialsError:
            return ResponseContents(
                import_status="password_required",
                message="Configuration file is protected with a password. "
                "Please enter the password",
                status_code=403,
            ).form_response()

    @staticmethod
    def import_config(config_json):
        if not ConfigService.update_config(config_json, should_encrypt=True):
            raise InvalidConfigurationError
