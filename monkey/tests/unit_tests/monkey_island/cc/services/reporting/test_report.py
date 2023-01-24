from datetime import datetime
from ipaddress import IPv4Address, IPv4Interface
from unittest.mock import MagicMock
from uuid import UUID

import pytest
import pytz
from tests.monkey_island import (
    InMemoryAgentConfigurationRepository,
    InMemoryAgentEventRepository,
    InMemoryAgentPluginRepository,
    InMemoryAgentRepository,
)

from common.agent_events import (
    AgentShutdownEvent,
    ExploitationEvent,
    PasswordRestorationEvent,
    PropagationEvent,
)
from common.types import SocketAddress
from monkey_island.cc.models import Agent, CommunicationType, Machine, Node
from monkey_island.cc.repositories import IAgentEventRepository, IAgentRepository
from monkey_island.cc.services.reporting.report import ReportService

EVENT_1 = AgentShutdownEvent(source=UUID("2d56f972-78a8-4026-9f47-2dfd550ee207"), timestamp=10)
EVENT_2 = ExploitationEvent(
    source=UUID("2d56f972-78a8-4026-9f47-2dfd550ee207"),
    target=IPv4Address("1.1.1.1"),
    success=False,
    exploiter_name="ssh",
    timestamp=1,
)
EVENT_3 = ExploitationEvent(
    source=UUID("2d56f972-78a8-4026-9f47-2dfd550ee207"),
    target=IPv4Address("1.1.1.1"),
    success=True,
    exploiter_name="ssh",
    timestamp=2,
)
EVENT_4 = PropagationEvent(
    source=UUID("2d56f972-78a8-4026-9f47-2dfd550ee207"),
    target=IPv4Address("1.1.1.1"),
    success=True,
    exploiter_name="ssh",
    timestamp=3,
)
EVENT_5 = PasswordRestorationEvent(
    source=UUID("2d56f972-78a8-4026-9f47-2dfd550ee207"),
    target=IPv4Address("1.1.1.1"),
    success=True,
    timestamp=4,
)

EVENT_6 = ExploitationEvent(
    source=UUID("2d56f972-78a8-4026-9f47-2dfd550ee207"),
    target=IPv4Address("2.2.2.2"),
    success=False,
    exploiter_name="wmi",
    timestamp=11,
)
EVENTS = [EVENT_2, EVENT_3, EVENT_4, EVENT_1, EVENT_5]

ISLAND_MACHINE = Machine(
    id=99,
    island=True,
    hostname="Island",
    hardware_id=5,
    network_interfaces=[IPv4Interface("10.10.10.99/24")],
)

MACHINE_1 = Machine(
    id=1,
    hardware_id=9,
    hostname="machine_1",
    network_interfaces=[IPv4Interface("10.10.10.1/24")],
)

MACHINE_2 = Machine(
    id=2,
    hardware_id=9,
    network_interfaces=[IPv4Interface("10.10.10.2/24")],
)

MACHINE_3 = Machine(
    id=3,
    hardware_id=9,
    network_interfaces=[IPv4Interface("10.10.10.3/24")],
)

AGENTS = [
    Agent(
        id=UUID("2d56f972-78a8-4026-9f47-2dfd550ee207"),
        machine_id=1,
        start_time=100,
        stop_time=500,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
    ),
    Agent(
        id=UUID("65c641f2-af47-4a42-929b-109b30f0d8d6"),
        machine_id=2,
        start_time=200,
        stop_time=600,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
    ),
    Agent(
        id=UUID("290da3c3-f410-4f5e-a472-b04416860a2c"),
        machine_id=3,
        start_time=300,
        stop_time=700,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
    ),
    Agent(
        id=UUID("e5cd334a-5ca5-4f19-a2ab-a68d515fea46"),
        machine_id=1,
        start_time=600,
        stop_time=40309,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
    ),
]

AGENT_NOT_DEAD = Agent(
    id=UUID("10e603df-609f-42c6-af08-59c63e82b873"),
    machine_id=2,
    start_time=601,
    stop_time=None,
    cc_server=SocketAddress(ip="127.0.0.1", port=5000),
)


NODES = [
    Node(
        machine_id=1,
        connections={"2": frozenset([CommunicationType.EXPLOITED, CommunicationType.SCANNED])},
    ),
    Node(machine_id=99, connections={"1": frozenset([CommunicationType.SCANNED])}),
    Node(
        machine_id=3,
        connections={"99": frozenset([CommunicationType.CC, CommunicationType.EXPLOITED])},
    ),
]

MACHINES = [MACHINE_1, MACHINE_2, MACHINE_3, ISLAND_MACHINE]

EXPECTED_SCANNED_MACHINES = [
    {
        "hostname": MACHINE_1.hostname,
        "ip_addresses": [str(iface.ip) for iface in MACHINE_1.network_interfaces],
        "accessible_from_nodes": [ISLAND_MACHINE.dict(simplify=True)],
        "services": [],
        "domain_name": "",
    },
    {
        "hostname": MACHINE_2.hostname,
        "ip_addresses": [str(iface.ip) for iface in MACHINE_2.network_interfaces],
        "accessible_from_nodes": [MACHINE_1.dict(simplify=True)],
        "services": [],
        "domain_name": "",
    },
]


def get_machine_by_id(machine_id):
    return [machine for machine in MACHINES if machine_id == machine.id][0]


@pytest.fixture
def agent_repository() -> IAgentRepository:
    repo = InMemoryAgentRepository()
    for agent in AGENTS:
        repo.upsert_agent(agent)

    return repo


@pytest.fixture
def agent_event_repository() -> IAgentEventRepository:
    repo = InMemoryAgentEventRepository()
    for event in EVENTS:
        repo.save_event(event)

    return repo


@pytest.fixture(autouse=True)
def report_service(
    agent_repository: IAgentRepository, agent_event_repository: IAgentEventRepository
):
    ReportService._machine_repository = MagicMock()
    ReportService._machine_repository.get_machines.return_value = MACHINES
    ReportService._machine_repository.get_machine_by_id = get_machine_by_id
    ReportService._agent_repository = agent_repository
    ReportService._node_repository = MagicMock()
    ReportService._node_repository.get_nodes.return_value = NODES
    ReportService._agent_event_repository = agent_event_repository
    ReportService._agent_configuration_repository = InMemoryAgentConfigurationRepository()
    ReportService._agent_plugin_repository = InMemoryAgentPluginRepository()


def test_get_scanned():
    scanned = ReportService.get_scanned()
    assert scanned == EXPECTED_SCANNED_MACHINES


def test_get_first_monkey_time():
    assert ReportService.get_first_monkey_time() == datetime.fromtimestamp(100, tz=pytz.UTC)


def test_get_last_monkey_time():
    assert ReportService.get_last_monkey_dead_time() == datetime.fromtimestamp(40309, tz=pytz.UTC)


def test_get_last_monkey_time__none():
    ReportService._agent_repository.upsert_agent(AGENT_NOT_DEAD)
    assert ReportService.get_last_monkey_dead_time() is None


def test_get_monkey_duration():
    assert ReportService.get_monkey_duration() == "11 hours, 10 minutes and 9 seconds"


def test_get_monkey_duration__none():
    ReportService._agent_repository.upsert_agent(AGENT_NOT_DEAD)
    assert ReportService.get_last_monkey_dead_time() is None


def test_report_service_agent_event_repository_error():
    ReportService._agent_event_repository = None
    with pytest.raises(RuntimeError):
        ReportService.get_latest_event_timestamp()


def test_report_service_get_latest_event_timestamp():
    latest_event_timestamp = ReportService.get_latest_event_timestamp()
    assert latest_event_timestamp == EVENT_1.timestamp


def test_report_generation(monkeypatch, agent_event_repository):
    monkeypatch.setattr(ReportService, "get_issues", lambda: [])
    monkeypatch.setattr(ReportService, "get_cross_segment_issues", lambda: [])

    ReportService.update_report()
    actual_report = ReportService.get_report()
    agent_event_repository.save_event(EVENT_6)

    ReportService.update_report()
    generated_report = ReportService.get_report()
    assert actual_report != generated_report
    assert actual_report["meta_info"]["latest_event_timestamp"] == EVENT_1.timestamp
    assert generated_report["meta_info"]["latest_event_timestamp"] == EVENT_6.timestamp

    ReportService.update_report()
    cached_report = ReportService.get_report()
    assert generated_report == cached_report
    assert cached_report["meta_info"]["latest_event_timestamp"] == EVENT_6.timestamp


def test_report_generation__no_agent_repository():
    ReportService._agent_repository = None

    with pytest.raises(RuntimeError):
        ReportService.update_report()
