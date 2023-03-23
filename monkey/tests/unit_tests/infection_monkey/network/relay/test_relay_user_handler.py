from ipaddress import IPv4Address
from time import sleep

import pytest

from infection_monkey.network.relay import RelayUserHandler

USER_ADDRESS = IPv4Address("0.0.0.0")


@pytest.fixture
def handler():
    return RelayUserHandler()


def test_potential_users_added(handler):
    assert not handler.has_potential_users()
    handler.add_potential_user(USER_ADDRESS)
    assert handler.has_potential_users()


def test_potential_user_removed_on_matching_user_added(handler):
    handler.add_potential_user(USER_ADDRESS)
    handler.add_relay_user(USER_ADDRESS)

    assert not handler.has_potential_users()


def test_potential_users_time_out():
    handler = RelayUserHandler(new_client_timeout=0.0001)

    handler.add_potential_user(USER_ADDRESS)
    sleep(0.02)

    assert not handler.has_potential_users()


def test_relay_users_added(handler):
    assert not handler.has_connected_users()
    handler.add_relay_user(USER_ADDRESS)
    assert handler.has_connected_users()


def test_relay_users_time_out():
    handler = RelayUserHandler(client_disconnect_timeout=0.001)

    handler.add_relay_user(USER_ADDRESS)
    sleep(0.01)

    assert not handler.has_connected_users()
