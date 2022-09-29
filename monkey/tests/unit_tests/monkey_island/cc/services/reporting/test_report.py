from ipaddress import IPv4Interface

from monkey_island.cc.models import CommunicationType, Machine, Node

ISLAND_MACHINE = Machine(
    id=99,
    island=True,
    hardware_id=5,
    network_interfaces=[IPv4Interface("10.10.10.99/24")],
)

MACHINE_A = Machine(
    id=1,
    hardware_id=9,
    network_interfaces=[IPv4Interface("10.10.10.1/24")],
)

MACHINE_B = Machine(
    id=2,
    hardware_id=9,
    network_interfaces=[IPv4Interface("10.10.10.2/24")],
)

MACHINE_C = Machine(
    id=3,
    hardware_id=9,
    network_interfaces=[IPv4Interface("10.10.10.3/24")],
)

NODES = [
    Node(machine_id=1, connections={"2": {CommunicationType.EXPLOITED}}),
    Node(machine_id=99, connections={"1": {CommunicationType.SCANNED}}),
    Node(machine_id=3, connections={"99": {CommunicationType.CC}}),
]
