from pathlib import Path

from flask import Flask
from flask_limiter import Limiter
from flask_security import Security
from ophidian import DIContainer

from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from . import IOTPGenerator
from .authentication_facade import AuthenticationFacade
from .authentication_service_otp_generator import AuthenticationServiceOTPGenerator
from .configure_flask_security import configure_flask_security
from .flask_resources import register_resources
from .mongo_otp_repository import MongoOTPRepository
from .register_event_handlers import register_event_handlers


def setup_authentication(api, app: Flask, container: DIContainer, data_dir: Path, limiter: Limiter):
    security = configure_flask_security(app, data_dir)

    authentication_facade = _build_authentication_facade(container, security)
    otp_generator = AuthenticationServiceOTPGenerator(authentication_facade)
    container.register_instance(IOTPGenerator, otp_generator)

    register_event_handlers(container, authentication_facade)
    register_resources(api, authentication_facade, otp_generator, limiter)

    # revoke all old tokens so that the user has to log in again on startup
    authentication_facade.revoke_all_tokens_for_all_users()
    authentication_facade.revoke_all_otps()


def _build_authentication_facade(container: DIContainer, security: Security):
    repository_encryptor = container.resolve(ILockableEncryptor)
    island_event_queue = container.resolve(IIslandEventQueue)

    return AuthenticationFacade(
        repository_encryptor,
        island_event_queue,
        security.datastore,
        container.resolve(MongoOTPRepository),
        security.app.config["SECURITY_TOKEN_MAX_AGE"],
    )
