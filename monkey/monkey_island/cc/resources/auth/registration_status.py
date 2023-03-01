from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services import AuthenticationService


class RegistrationStatus(AbstractResource):

    urls = ["/api/registration-status"]

    def __init__(self, authentication_service: AuthenticationService):
        self._authentication_service = authentication_service

    def get(self):
        return {"needs_registration": self._authentication_service.needs_registration()}
