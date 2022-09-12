from common import DIContainer
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.island_event_handlers import reset_agent_configuration
from monkey_island.cc.repository import ICredentialsRepository


def setup_island_event_handlers(container: DIContainer):
    event_queue = container.resolve(IIslandEventQueue)

    _handle_reset_agent_configuration_events(event_queue, container)
    _handle_clear_simulation_data_events(event_queue, container)


def _handle_reset_agent_configuration_events(
    event_queue: IIslandEventQueue, container: DIContainer
):
    event_queue.subscribe(
        IslandEventTopic.RESET_AGENT_CONFIGURATION, container.resolve(reset_agent_configuration)
    )


def _handle_clear_simulation_data_events(event_queue: IIslandEventQueue, container: DIContainer):
    credentials_repository = container.resolve(ICredentialsRepository)

    event_queue.subscribe(
        IslandEventTopic.CLEAR_SIMULATION_DATA, credentials_repository.remove_stolen_credentials
    )
