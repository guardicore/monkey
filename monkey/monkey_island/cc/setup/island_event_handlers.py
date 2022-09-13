from functools import partial

from common import DIContainer
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.island_event_handlers import reset_agent_configuration
from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.services.database import Database


def setup_island_event_handlers(container: DIContainer):
    island_event_queue = container.resolve(IIslandEventQueue)

    _subscribe_reset_agent_configuration_events(island_event_queue, container)
    _subscribe_clear_simulation_data_events(island_event_queue, container)


def _subscribe_reset_agent_configuration_events(
    island_event_queue: IIslandEventQueue, container: DIContainer
):
    island_event_queue.subscribe(
        IslandEventTopic.RESET_AGENT_CONFIGURATION, container.resolve(reset_agent_configuration)
    )


def _subscribe_clear_simulation_data_events(
    island_event_queue: IIslandEventQueue, container: DIContainer
):
    legacy_database_reset = partial(Database.reset_db, reset_config=False)
    island_event_queue.subscribe(IslandEventTopic.CLEAR_SIMULATION_DATA, legacy_database_reset)

    credentials_repository = container.resolve(ICredentialsRepository)
    island_event_queue.subscribe(
        IslandEventTopic.CLEAR_SIMULATION_DATA, credentials_repository.remove_stolen_credentials
    )
