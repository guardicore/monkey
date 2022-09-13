from common import DIContainer
from monkey_island.cc.event_queue import IslandEventTopic, PyPubSubIslandEventQueue
from monkey_island.cc.island_event_handlers import reset_agent_configuration


def setup_island_event_handlers(container: DIContainer):
    event_queue = container.resolve(PyPubSubIslandEventQueue)

    event_queue.subscribe(
        IslandEventTopic.RESET_AGENT_CONFIGURATION, container.resolve(reset_agent_configuration)
    )
