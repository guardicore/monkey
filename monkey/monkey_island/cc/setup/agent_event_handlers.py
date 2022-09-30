from common import DIContainer
from common.agent_events import CredentialsStolenEvent, PingScanEvent, TCPScanEvent
from common.event_queue import IAgentEventQueue
from monkey_island.cc.agent_event_handlers import (
    ScanEventHandler,
    save_event_to_event_repository,
    save_stolen_credentials_to_repository,
)
from monkey_island.cc.repository import (
    IAgentEventRepository,
    IAgentRepository,
    ICredentialsRepository,
    IMachineRepository,
    INodeRepository,
)


def setup_agent_event_handlers(container: DIContainer):
    _subscribe_and_store_to_event_repository(container)
    _subscribe_scan_events(container)


def _subscribe_and_store_to_event_repository(container: DIContainer):
    agent_event_queue = container.resolve(IAgentEventQueue)

    save_event_subscriber = save_event_to_event_repository(container.resolve(IAgentEventRepository))
    agent_event_queue.subscribe_all_events(save_event_subscriber)

    save_stolen_credentials_subscriber = save_stolen_credentials_to_repository(
        container.resolve(ICredentialsRepository)
    )
    agent_event_queue.subscribe_type(CredentialsStolenEvent, save_stolen_credentials_subscriber)


def _subscribe_scan_events(container: DIContainer):
    agent_event_queue = container.resolve(IAgentEventQueue)
    agent_repository = container.resolve(IAgentRepository)
    machine_repository = container.resolve(IMachineRepository)
    node_repository = container.resolve(INodeRepository)

    scan_event_handler = ScanEventHandler(agent_repository, machine_repository, node_repository)

    agent_event_queue.subscribe_type(PingScanEvent, scan_event_handler.handle_ping_scan_event)
    agent_event_queue.subscribe_type(TCPScanEvent, scan_event_handler.handle_tcp_scan_event)
