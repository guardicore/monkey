from pathlib import Path

from flask import Flask
from flask_limiter import Limiter
from flask_security import Security

from common import DIContainer
from common.agent_events import AbstractAgentEvent, AgentShutdownEvent
from common.event_queue import IAgentEventQueue
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from . import IOTPGenerator
from .authentication_facade import AuthenticationFacade
from .authentication_service_otp_generator import AuthenticationServiceOTPGenerator
from .configure_flask_security import configure_flask_security
from .flask_resources import register_resources
from .mongo_otp_repository import MongoOTPRepository
from .token_generator import TokenGenerator
from .token_parser import TokenParser

# TODO:
# - Subscribe to the agent timeout event
# - Subscribe to the agent shutdown event
# - Handle the events by removing the agent user from the datastore


def setup_authentication(api, app: Flask, container: DIContainer, data_dir: Path, limiter: Limiter):
    security = configure_flask_security(app, data_dir)

    authentication_facade = _build_authentication_facade(container, security)
    otp_generator = AuthenticationServiceOTPGenerator(authentication_facade)
    container.register_instance(IOTPGenerator, otp_generator)

    _register_event_handlers(container, authentication_facade)
    register_resources(api, authentication_facade, otp_generator, limiter)

    # revoke all old tokens so that the user has to log in again on startup
    authentication_facade.revoke_all_tokens_for_all_users()


def _build_authentication_facade(container: DIContainer, security: Security):
    repository_encryptor = container.resolve(ILockableEncryptor)
    island_event_queue = container.resolve(IIslandEventQueue)

    token_generator = TokenGenerator(security)
    refresh_token_expiration = (
        security.app.config["SECURITY_TOKEN_MAX_AGE"]
        + security.app.config["SECURITY_REFRESH_TOKEN_TIMEDELTA"]
    )
    token_parser = TokenParser(security, refresh_token_expiration)

    return AuthenticationFacade(
        repository_encryptor,
        island_event_queue,
        security.datastore,
        token_generator,
        token_parser,
        container.resolve(MongoOTPRepository),
    )


def _register_event_handlers(container: DIContainer, authentication_facade: AuthenticationFacade):
    agent_event_queue = container.resolve(IAgentEventQueue)
    island_event_queue = container.resolve(IIslandEventQueue)

    agent_event_queue.subscribe_type(
        AgentShutdownEvent, unregister_agent_on_shutdown(authentication_facade)
    )
    island_event_queue.subscribe(
        IslandEventTopic.AGENT_TIMED_OUT, unregister_agent_on_timeout(authentication_facade)
    )


class unregister_agent_on_shutdown:
    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def __call__(self, event: AbstractAgentEvent):
        agent_id = event.source
        self._authentication_facade.remove_user(str(agent_id))


class unregister_agent_on_timeout:
    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def __call__(self, agent_id: str):
        self._authentication_facade.remove_user(agent_id)
