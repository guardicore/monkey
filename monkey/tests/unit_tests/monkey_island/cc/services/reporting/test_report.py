from ipaddress import IPv4Interface
from unittest.mock import MagicMock

from monkey_island.cc.models import CommunicationType, Machine, Node
from monkey_island.cc.services.reporting.report import ReportService

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
        "ip_addresses": MACHINE_1.network_interfaces,
        "accessible_from_nodes": [ISLAND_MACHINE],
        "services": [],
        "domain_name": "",
    },
    {
        "hostname": MACHINE_2.hostname,
        "ip_addresses": MACHINE_2.network_interfaces,
        "accessible_from_nodes": [MACHINE_1],
        "services": [],
        "domain_name": "",
    },
]


def get_machine_by_id(machine_id):
    return [machine for machine in MACHINES if machine_id == machine.id][0]


def test_get_scanned():
    ReportService._node_repository = MagicMock()
    ReportService._node_repository.get_nodes.return_value = NODES
    ReportService._machine_repository = MagicMock()
    ReportService._machine_repository.get_machines.return_value = MACHINES
    ReportService._machine_repository.get_machine_by_id = get_machine_by_id
    scanned = ReportService.get_scanned()
    assert scanned == EXPECTED_SCANNED_MACHINES
