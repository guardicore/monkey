from monkey_island.cc.flask_utils import AbstractResource

from ..authentication_facade import AuthenticationFacade


class RegistrationStatus(AbstractResource):
    urls = ["/api/registration-status"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    # Can't be secured, used before registration
    def get(self):
        return {"needs_registration": self._authentication_facade.needs_registration()}
