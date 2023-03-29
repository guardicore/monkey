from . import register_resources
from .authentication_facade import AuthenticationFacade


def setup_authentication(api, authentication_facade: AuthenticationFacade):
    register_resources(api, authentication_facade)
    # revoke all old tokens so that the user has to log in again on startup
    authentication_facade.revoke_all_tokens_for_all_users()
