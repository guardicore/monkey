from http import HTTPStatus

from flask import request

from common.credentials import Credentials
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import ICredentialsRepository

_configured_collection = "configured-credentials"
_stolen_collection = "stolen-credentials"


class PropagationCredentials(AbstractResource):
    urls = ["/api/propagation-credentials", "/api/propagation-credentials/<string:collection>"]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    # Used by Agent. Can't secure.
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

    # Used by Agent. Can't secure.
    def put(self, collection=None):
        credentials = [Credentials(**c) for c in request.json]
        if collection == _configured_collection:
            self._credentials_repository.remove_configured_credentials()
            self._credentials_repository.save_configured_credentials(credentials)
        elif collection is None or collection == _stolen_collection:
            return {}, HTTPStatus.METHOD_NOT_ALLOWED
        else:
            return {}, HTTPStatus.NOT_FOUND

        return {}, HTTPStatus.NO_CONTENT
