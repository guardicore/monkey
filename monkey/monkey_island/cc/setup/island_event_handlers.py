from functools import partial

from common import DIContainer
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.island_event_handlers import (
    reset_agent_configuration,
    reset_machine_repository,
    set_agent_configuration_per_island_mode,
    set_simulation_mode,
)
from monkey_island.cc.repository import (
    IAgentEventRepository,
    IAgentRepository,
    ICredentialsRepository,
    INodeRepository,
)
from monkey_island.cc.services.database import Database


def setup_island_event_handlers(container: DIContainer):
    island_event_queue = container.resolve(IIslandEventQueue)

    _subscribe_reset_agent_configuration_events(island_event_queue, container)
    _subscribe_clear_simulation_data_events(island_event_queue, container)
    _subscribe_set_island_mode_events(island_event_queue, container)


def _subscribe_reset_agent_configuration_events(
    island_event_queue: IIslandEventQueue, container: DIContainer
):
    topic = IslandEventTopic.RESET_AGENT_CONFIGURATION

    island_event_queue.subscribe(topic, container.resolve(reset_agent_configuration))


def _subscribe_clear_simulation_data_events(
    island_event_queue: IIslandEventQueue, container: DIContainer
):
    topic = IslandEventTopic.CLEAR_SIMULATION_DATA

    legacy_database_reset = partial(Database.reset_db, reset_config=False)
    island_event_queue.subscribe(topic, legacy_database_reset)

    credentials_repository = container.resolve(ICredentialsRepository)
    island_event_queue.subscribe(topic, credentials_repository.remove_stolen_credentials)

    island_event_queue.subscribe(topic, container.resolve(reset_machine_repository))

    for i_repository in [
        INodeRepository,
        IAgentEventRepository,
        IAgentRepository,
    ]:
        repository = container.resolve(i_repository)
        island_event_queue.subscribe(topic, repository.reset)


def _subscribe_set_island_mode_events(
    island_event_queue: IIslandEventQueue, container: DIContainer
):
    topic = IslandEventTopic.SET_ISLAND_MODE

    island_event_queue.subscribe(topic, container.resolve(set_agent_configuration_per_island_mode))

    island_event_queue.subscribe(topic, container.resolve(set_simulation_mode))
