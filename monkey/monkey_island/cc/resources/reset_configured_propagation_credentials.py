from flask import make_response

from monkey_island.cc.repository import RemovalError
from monkey_island.cc.repository.i_credentials_repository import ICredentialsRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class ResetConfiguredPropagationCredentials(AbstractResource):
    urls = ["/api/reset-configured-propagation-credentials"]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    @jwt_required
    def post(self):
        """
        Reset propagation credentials that were configured by the user
        """
        try:
            self._credentials_repository.remove_configured_credentials()
        except RemovalError as err:
            make_response(
                {"error": f"Error encountered while removing configured credentials: {err}"}, 400
            )

        return make_response({}, 200)
