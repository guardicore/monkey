from flask import jsonify, request

from common.credentials import Credentials
from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource


class PropagationCredentials(AbstractResource):
    urls = ["/api/propagation-credentials"]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def get(self):
        origin = request.args.get("origin")
        propagation_credentials = self._credentials_repository.get_credentials(origin)

        return jsonify(propagation_credentials)

    def post(self):
        origin = request.args.get("origin")
        credentials = Credentials.from_mapping(request.json)
        self._credentials_repository.save_credentials(credentials, origin)

    def delete(self):
        origin = request.args.get("origin")
        self._credentials_repository.remove_credentials(origin)
