from ipaddress import IPv4Address
from threading import Thread

import pytest

from monkey.infection_monkey.tcp_relay import RELAY_CONTROL_MESSAGE, TCPRelay

NEW_USER_ADDRESS = IPv4Address("0.0.0.1")
LOCAL_PORT = 9975
TARGET_ADDRESS = "0.0.0.0"
TARGET_PORT = 9976


@pytest.fixture
def tcp_relay():
    return TCPRelay(LOCAL_PORT, TARGET_ADDRESS, TARGET_PORT)


def join_or_kill_thread(thread: Thread, timeout: float):
    """Whether or not the thread joined in the given timeout period."""
    thread.join(timeout)
    if thread.is_alive():
        # Cannot set daemon status of active thread: thread.daemon = True
        return False
    return True


# This will fail unless TcpProxy is updated to do non-blocking accepts
# def test_stops():
#     relay = TCPRelay(9975, "0.0.0.0", 9976)
#     relay.start()
#     relay.stop()

#     assert join_or_kill_thread(relay, 0.2)


def test_user_added(tcp_relay):
    tcp_relay.add_relay_user(NEW_USER_ADDRESS)

    users = tcp_relay.relay_users()
    assert len(users) == 1
    assert NEW_USER_ADDRESS in users


def test_user_removed_on_request(tcp_relay):
    tcp_relay.add_relay_user(NEW_USER_ADDRESS)
    tcp_relay.on_user_data_received(RELAY_CONTROL_MESSAGE, NEW_USER_ADDRESS)

    users = tcp_relay.relay_users()
    assert len(users) == 0


# This will fail unless TcpProxy is updated to do non-blocking accepts
# @pytest.mark.slow
# def test_waits_for_exploited_machines():
#     relay = TCPRelay(9975, "0.0.0.0", 9976, new_client_timeout=0.2)
#     new_user = "0.0.0.1"
#     relay.start()

#     relay.add_potential_user(new_user)
#     relay.stop()

#     assert not join_or_kill_thread(relay, 0.1)  # Should be waiting
#     assert join_or_kill_thread(relay, 1)  # Should be done waiting
