from common import DIContainer

from .authentication_service import AuthenticationService


def build(container: DIContainer) -> AuthenticationService:
    return container.resolve(AuthenticationService)
