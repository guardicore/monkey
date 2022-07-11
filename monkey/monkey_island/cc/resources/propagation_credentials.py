from http import HTTPStatus

from flask import make_response, request

from common.credentials import Credentials
from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource


class PropagationCredentials(AbstractResource):
    urls = [
        "/api/propagation-credentials",
        "/api/propagation-credentials/configured-credentials",
        "/api/propagation-credentials/stolen-credentials",
    ]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def get(self):
        propagation_credentials = []

        if request.url.endswith("/configured-credentials"):
            propagation_credentials = self._credentials_repository.get_configured_credentials()
        elif request.url.endswith("/stolen-credentials"):
            propagation_credentials = self._credentials_repository.get_stolen_credentials()
        else:
            propagation_credentials = self._credentials_repository.get_all_credentials()

        return make_response(Credentials.to_json_array(propagation_credentials), HTTPStatus.OK)

    def post(self):
        credentials = [Credentials.from_json(c) for c in request.json]

        if request.url.endswith("/configured-credentials"):
            self._credentials_repository.save_configured_credentials(credentials)
        elif request.url.endswith("/stolen-credentials"):
            self._credentials_repository.save_stolen_credentials(credentials)
        else:
            return {}, HTTPStatus.METHOD_NOT_ALLOWED

        return {}, HTTPStatus.NO_CONTENT

    def delete(self):
        if request.url.endswith("/configured-credentials"):
            self._credentials_repository.remove_configured_credentials()
        elif request.url.endswith("/stolen-credentials"):
            self._credentials_repository.remove_stolen_credentials()
        else:
            return {}, HTTPStatus.METHOD_NOT_ALLOWED

        return {}, HTTPStatus.NO_CONTENT
