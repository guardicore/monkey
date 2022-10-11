from common import DIContainer
from common.agent_events import (
    AgentShutdownEvent,
    CredentialsStolenEvent,
    ExploitationEvent,
    PingScanEvent,
    TCPScanEvent,
)
from common.event_queue import IAgentEventQueue
from monkey_island.cc.agent_event_handlers import (
    ScanEventHandler,
    save_event_to_event_repository,
    save_stolen_credentials_to_repository,
    update_agent_shutdown_status,
    update_nodes_on_exploitation,
)
from monkey_island.cc.repository import IAgentEventRepository, ICredentialsRepository


def setup_agent_event_handlers(container: DIContainer):
    agent_event_queue = container.resolve(IAgentEventQueue)

    _subscribe_and_store_to_event_repository(container)
    _subscribe_scan_events(container)
    _subscribe_exploitation_events(container, agent_event_queue)


def _subscribe_and_store_to_event_repository(container: DIContainer):
    agent_event_queue = container.resolve(IAgentEventQueue)

    # TODO: Can't we just `container.resolve(save_event_to_event_repository)`?
    save_event_subscriber = save_event_to_event_repository(container.resolve(IAgentEventRepository))
    agent_event_queue.subscribe_all_events(save_event_subscriber)

    save_stolen_credentials_subscriber = save_stolen_credentials_to_repository(
        container.resolve(ICredentialsRepository)
    )
    agent_event_queue.subscribe_type(CredentialsStolenEvent, save_stolen_credentials_subscriber)
    agent_event_queue.subscribe_type(AgentShutdownEvent, update_agent_shutdown_status)


def _subscribe_scan_events(container: DIContainer):
    agent_event_queue = container.resolve(IAgentEventQueue)
    scan_event_handler = container.resolve(ScanEventHandler)

    agent_event_queue.subscribe_type(PingScanEvent, scan_event_handler.handle_ping_scan_event)
    agent_event_queue.subscribe_type(TCPScanEvent, scan_event_handler.handle_tcp_scan_event)


def _subscribe_exploitation_events(container: DIContainer, agent_event_queue: IAgentEventQueue):
    agent_event_queue.subscribe_type(
        ExploitationEvent, container.resolve(update_nodes_on_exploitation)
    )
