import json
import logging
from dataclasses import dataclass
from json.decoder import JSONDecodeError

import flask_restful
from flask import request

from common.utils.exceptions import InvalidConfigurationError
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.server_utils.encryption import (
    InvalidCiphertextError,
    InvalidCredentialsError,
    PasswordBasedStringEncryptor,
    is_encrypted,
)
from monkey_island.cc.services.config import ConfigService

logger = logging.getLogger(__name__)


class ImportStatuses:
    UNSAFE_OPTION_VERIFICATION_REQUIRED = "unsafe_options_verification_required"
    INVALID_CONFIGURATION = "invalid_configuration"
    INVALID_CREDENTIALS = "invalid_credentials"
    IMPORTED = "imported"


@dataclass
class ResponseContents:
    import_status: str = ImportStatuses.IMPORTED
    message: str = ""
    status_code: int = 200
    config: str = ""
    config_schema: str = ""

    def form_response(self):
        return self.__dict__


class ConfigurationImport(flask_restful.Resource):
    SUCCESS = False

    @jwt_required
    def post(self):
        request_contents = json.loads(request.data)
        try:
            config = ConfigurationImport._get_plaintext_config_from_request(request_contents)
            if request_contents["unsafeOptionsVerified"]:
                ConfigurationImport.import_config(config)
                return ResponseContents().form_response()
            else:
                return ResponseContents(
                    config=json.dumps(config),
                    config_schema=ConfigService.get_config_schema(),
                    import_status=ImportStatuses.UNSAFE_OPTION_VERIFICATION_REQUIRED,
                ).form_response()
        except InvalidCredentialsError:
            return ResponseContents(
                import_status=ImportStatuses.INVALID_CREDENTIALS,
                message="Invalid credentials provided",
            ).form_response()
        except InvalidConfigurationError:
            return ResponseContents(
                import_status=ImportStatuses.INVALID_CONFIGURATION,
                message="Invalid configuration supplied. "
                "Maybe the format is outdated or the file has been corrupted.",
            ).form_response()

    @staticmethod
    def _get_plaintext_config_from_request(request_contents: dict) -> dict:
        try:
            config = request_contents["config"]
            if ConfigurationImport.is_config_encrypted(request_contents["config"]):
                pb_encryptor = PasswordBasedStringEncryptor(request_contents["password"])
                config = pb_encryptor.decrypt(config)
            return json.loads(config)
        except (JSONDecodeError, InvalidCiphertextError):
            logger.exception(
                "Exception encountered when trying to extract plaintext configuration."
            )
            raise InvalidConfigurationError

    @staticmethod
    def import_config(config_json):
        if not ConfigService.update_config(config_json, should_encrypt=True):
            raise InvalidConfigurationError

    @staticmethod
    def is_config_encrypted(config: str):
        try:
            if config.startswith("{"):
                return False
            elif is_encrypted(config):
                return True
            else:
                raise InvalidConfigurationError
        except Exception:
            raise InvalidConfigurationError
