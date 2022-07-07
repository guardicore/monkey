from flask import jsonify

from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource


class PropagationCredentials(AbstractResource):
    urls = ["/api/propagation-credentials"]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def get(self):
        propagation_credentials = self._credentials_repository.get_all_credentials()

        return jsonify(propagation_credentials)
