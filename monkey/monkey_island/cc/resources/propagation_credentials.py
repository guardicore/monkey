from http import HTTPStatus

from flask import request
from flask_security import auth_token_required, roles_accepted
from monkeytypes import Credentials

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import ICredentialsRepository
from monkey_island.cc.services.authentication_service import AccountRole

_configured_collection = "configured-credentials"
_stolen_collection = "stolen-credentials"


class PropagationCredentials(AbstractResource):
    urls = ["/api/propagation-credentials", "/api/propagation-credentials/<string:collection>"]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    @auth_token_required
    @roles_accepted(AccountRole.AGENT.name, AccountRole.ISLAND_INTERFACE.name)
    def get(self, collection=None):
        if collection == _configured_collection:
            propagation_credentials = self._credentials_repository.get_configured_credentials()
        elif collection == _stolen_collection:
            propagation_credentials = self._credentials_repository.get_stolen_credentials()
        elif collection is None:
            propagation_credentials = self._credentials_repository.get_all_credentials()
        else:
            return {}, HTTPStatus.NOT_FOUND

        return propagation_credentials, HTTPStatus.OK

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def put(self, collection=None):
        try:
            credentials = []
            for credential_pair in request.json:
                credentials.append(Credentials(**credential_pair))
        except (TypeError, ValueError) as err:
            return {
                "error": {
                    "message": f"{str(err)}",
                    "bad_input": f"{credential_pair}"
                    }
                }, HTTPStatus.BAD_REQUEST

        if collection == _configured_collection:
            self._credentials_repository.remove_configured_credentials()
            self._credentials_repository.save_configured_credentials(credentials)
        elif collection is None or collection == _stolen_collection:
            return {}, HTTPStatus.METHOD_NOT_ALLOWED
        else:
            return {}, HTTPStatus.NOT_FOUND

        return {}, HTTPStatus.NO_CONTENT
