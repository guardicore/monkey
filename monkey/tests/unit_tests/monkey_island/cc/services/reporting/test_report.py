from copy import deepcopy
from datetime import datetime
from ipaddress import IPv4Address, IPv4Interface
from unittest.mock import MagicMock
from uuid import UUID

import pytest
import pytz
from monkeytypes import AgentPluginType
from tests.data_for_tests.agent_plugin.manifests import (
    EXPLOITER_INCOMPLETE_MANIFEST,
    EXPLOITER_NAME_1,
    EXPLOITER_NAME_2,
    PLUGIN_MANIFESTS,
    REMEDIATION_SUGGESTION_1,
    REMEDIATION_SUGGESTION_2,
)
from tests.monkey_island import (
    InMemoryAgentConfigurationService,
    InMemoryAgentEventRepository,
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
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService
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
    exploiter_name="exploiter one",
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

AGENT_SHA256 = "59e822fe452926447efb74fb980e885a84e5c26a0c6bb4ce0634f6982390d50b"
AGENTS = [
    Agent(
        id=UUID("2d56f972-78a8-4026-9f47-2dfd550ee207"),
        machine_id=1,
        start_time=100,
        stop_time=500,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
        sha256=AGENT_SHA256,
    ),
    Agent(
        id=UUID("65c641f2-af47-4a42-929b-109b30f0d8d6"),
        machine_id=2,
        start_time=200,
        stop_time=600,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
        sha256=AGENT_SHA256,
    ),
    Agent(
        id=UUID("290da3c3-f410-4f5e-a472-b04416860a2c"),
        machine_id=3,
        start_time=300,
        stop_time=700,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
        sha256=AGENT_SHA256,
    ),
    Agent(
        id=UUID("e5cd334a-5ca5-4f19-a2ab-a68d515fea46"),
        machine_id=1,
        start_time=600,
        stop_time=40309,
        cc_server=SocketAddress(ip="127.0.0.1", port=5000),
        sha256=AGENT_SHA256,
    ),
]

AGENT_NOT_DEAD = Agent(
    id=UUID("10e603df-609f-42c6-af08-59c63e82b873"),
    machine_id=2,
    start_time=601,
    stop_time=None,
    cc_server=SocketAddress(ip="127.0.0.1", port=5000),
    sha256=AGENT_SHA256,
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
        "accessible_from_nodes": [ISLAND_MACHINE.to_json_dict()],
        "services": [],
        "domain_name": "",
    },
    {
        "hostname": MACHINE_2.hostname,
        "ip_addresses": [str(iface.ip) for iface in MACHINE_2.network_interfaces],
        "accessible_from_nodes": [MACHINE_1.to_json_dict()],
        "services": [],
        "domain_name": "",
    },
]

ISSUE_1 = {
    "machine_id": 8,
    "machine": "hadoop-2",
    "ip_address": "10.2.2.2",
    "type": EXPLOITER_NAME_1,
    "password_restored": None,
}

ISSUE_2 = {
    "machine_id": 9,
    "machine": "hadoop-3",
    "ip_address": "10.2.2.3",
    "type": EXPLOITER_NAME_2,
    "password_restored": True,
}

ISSUE_3 = {
    "machine_id": 10,
    "machine": "hadoop-4",
    "ip_address": "10.2.2.4",
    "type": EXPLOITER_INCOMPLETE_MANIFEST,
    "password_restored": True,
}

ISSUE_4 = {
    "machine_id": 10,
    "machine": "hadoop-4",
    "ip_address": "10.2.2.4",
    "type": "non existent",
    "password_restored": True,
}


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


@pytest.fixture
def mock_agent_plugin_service() -> IAgentPluginService:
    return MagicMock(spec=IAgentPluginService)


@pytest.fixture(autouse=True)
def report_service(
    agent_repository: IAgentRepository,
    agent_event_repository: IAgentEventRepository,
    mock_agent_plugin_service: IAgentPluginService,
):
    ReportService._machine_repository = MagicMock()
    ReportService._machine_repository.get_machines.return_value = MACHINES
    ReportService._machine_repository.get_machine_by_id = get_machine_by_id
    ReportService._agent_repository = agent_repository
    ReportService._node_repository = MagicMock()
    ReportService._node_repository.get_nodes.return_value = NODES
    ReportService._agent_event_repository = agent_event_repository
    ReportService._agent_configuration_service = InMemoryAgentConfigurationService()
    ReportService._agent_plugin_service = mock_agent_plugin_service


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
    monkeypatch.setattr(ReportService, "add_remediation_to_issue", lambda issue: issue)

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


@pytest.mark.parametrize(
    "issue, expected_remediation",
    [(ISSUE_1, REMEDIATION_SUGGESTION_1), (ISSUE_2, REMEDIATION_SUGGESTION_2), (ISSUE_3, None)],
)
def test_report__add_remediation_to_issue(issue, expected_remediation):
    issue = deepcopy(issue)
    manifest = PLUGIN_MANIFESTS[AgentPluginType.EXPLOITER][issue["type"]]

    issue_with_remediation = ReportService.add_remediation_to_issue(issue, manifest)

    assert issue_with_remediation["remediation_suggestion"] == expected_remediation


def test_report__add_remediation_to_issue_missing_manifest():
    manifest = None

    issue = ReportService.add_remediation_to_issue(deepcopy(ISSUE_1), manifest)

    assert "remediation_suggestion" not in issue
