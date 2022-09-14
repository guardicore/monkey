from common import DIContainer
from common.event_queue import IAgentEventQueue
from common.events import CredentialsStolenEvent
from monkey_island.cc.agent_event_subscribers import (
    save_event_to_event_repository,
    save_stolen_credentials_to_repository,
)
from monkey_island.cc.repository import ICredentialsRepository, IEventRepository


def setup_agent_event_handlers(container: DIContainer):
    _subscribe_and_store_to_event_repository(container)


def _subscribe_and_store_to_event_repository(container: DIContainer):
    agent_event_queue = container.resolve(IAgentEventQueue)

    event_repository = container.resolve(IEventRepository)
    save_event_subscriber = save_event_to_event_repository(event_repository)
    agent_event_queue.subscribe_all_events(save_event_subscriber)

    save_stolen_credentials_subscriber = save_stolen_credentials_to_repository(
        container.resolve(ICredentialsRepository)
    )
    agent_event_queue.subscribe_type(CredentialsStolenEvent, save_stolen_credentials_subscriber)
