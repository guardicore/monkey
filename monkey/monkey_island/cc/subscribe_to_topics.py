from common import DIContainer
from monkey_island.cc.event_queue import IslandEventTopic, PyPubSubIslandEventQueue
from monkey_island.cc.services.reset_agent_configuration import reset_agent_configuration


def subscribe_to_topics(container: DIContainer):
    event_queue = container.resolve(PyPubSubIslandEventQueue)

    event_queue.subscribe(
        IslandEventTopic.RESET_AGENT_CONFIGURATION, container.resolve(reset_agent_configuration)
    )
