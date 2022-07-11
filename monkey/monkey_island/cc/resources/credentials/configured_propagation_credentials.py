import logging

from flask import jsonify, request

from common.credentials import Credentials
from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class ConfiguredPropagationCredentials(AbstractResource):
    urls = ["/api/propagation-credentials/configured"]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def get(self):
        return jsonify(self._credentials_repository.get_configured_credentials())

    def post(self):
        credentials = Credentials.from_mapping(request.json)
        self._credentials_repository.save_configured_credentials(credentials)

    def delete(self):
        self._credentials_repository.remove_configured_credentials()
