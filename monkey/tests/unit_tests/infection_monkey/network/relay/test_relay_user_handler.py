from ipaddress import IPv4Address

from monkey.infection_monkey.network.relay import RelayUserHandler


def test_potential_users_added():
    user_address = IPv4Address("0.0.0.0")
    handler = RelayUserHandler()

    assert len(handler.get_potential_users()) == 0
    handler.add_potential_user(user_address)
    assert len(handler.get_potential_users()) == 1
    assert user_address in handler.get_potential_users()


def test_potential_user_removed_on_matching_user_added():
    user_address = IPv4Address("0.0.0.0")
    handler = RelayUserHandler()

    handler.add_potential_user(user_address)
    handler.add_relay_user(user_address)

    assert len(handler.get_potential_users()) == 0
