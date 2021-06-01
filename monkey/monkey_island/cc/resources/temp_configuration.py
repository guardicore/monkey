import json
from dataclasses import dataclass

import flask_restful
from flask import request

from common.utils.exceptions import (
    InvalidConfigurationError,
    InvalidCredentialsError,
    NoCredentialsError,
)
from monkey_island.cc.resources.auth.auth import jwt_required


@dataclass
class ResponseContents:
    import_status: str = "imported"
    message: str = ""
    status_code: int = 200

    def form_response(self):
        return self.__dict__, self.status_code


# TODO remove once backend implementation is done
class TempConfiguration(flask_restful.Resource):
    SUCCESS = False

    @jwt_required
    def post(self):
        request_contents = json.loads(request.data)
        try:
            self.decrypt(request_contents["password"])
            self.import_config()
            return ResponseContents().form_response()
        except InvalidCredentialsError:
            return ResponseContents(
                import_status="wrong_password", message="Wrong password supplied", status_code=403
            ).form_response()
        except InvalidConfigurationError:
            return ResponseContents(
                import_status="invalid_configuration",
                message="Invalid configuration supplied. "
                "Maybe the format is outdated or the file is malformed",
                status_code=400,
            ).form_response()
        except NoCredentialsError:
            return ResponseContents(
                import_status="password_required",
                message="Configuration file is protected with a password. "
                "Please enter the password",
                status_code=403,
            ).form_response()

    def decrypt(self, password=""):
        if not password:
            raise NoCredentialsError
        if not password == "abc":
            raise InvalidCredentialsError
        return False

    def import_config(self):
        return True
