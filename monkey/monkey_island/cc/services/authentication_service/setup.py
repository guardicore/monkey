from pathlib import Path

from flask_security import UserDatastore

from common import DIContainer
from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from . import register_resources
from .authentication_facade import AuthenticationFacade
from .configure_flask_security import configure_flask_security


def setup_authentication(app, api, data_dir: Path, container: DIContainer):
    datastore = configure_flask_security(app, data_dir)
    authentication_facade = _build_authentication_facade(container, datastore)
    register_resources(api, authentication_facade)


def _build_authentication_facade(container: DIContainer, user_datastore: UserDatastore):
    repository_encryptor = container.resolve(ILockableEncryptor)
    island_event_queue = container.resolve(IIslandEventQueue)
    return AuthenticationFacade(repository_encryptor, island_event_queue, user_datastore)
