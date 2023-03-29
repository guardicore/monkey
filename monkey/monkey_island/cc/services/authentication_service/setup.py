from flask_security import UserDatastore

from common import DIContainer
from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from . import register_resources
from .authentication_facade import AuthenticationFacade


def setup_authentication(api, datastore: UserDatastore, container: DIContainer):
    authentication_facade = _build_authentication_facade(container, datastore)
    register_resources(api, authentication_facade)
    # revoke all old tokens so that the user has to log in again on startup
    authentication_facade.revoke_all_tokens_for_all_users()


def _build_authentication_facade(container: DIContainer, user_datastore: UserDatastore):
    repository_encryptor = container.resolve(ILockableEncryptor)
    island_event_queue = container.resolve(IIslandEventQueue)
    return AuthenticationFacade(repository_encryptor, island_event_queue, user_datastore)
