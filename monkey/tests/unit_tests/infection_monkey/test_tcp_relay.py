from threading import Thread

from monkey.infection_monkey.tcp_relay import TCPRelay


def join_or_kill_thread(thread: Thread, timeout: float):
    thread.join(timeout)
    if thread.is_alive():
        thread.daemon = True
        return False
    return True


def test_stops():
    relay = TCPRelay(9975, "0.0.0.0", 9976)
    relay.start()
    relay.stop()

    assert join_or_kill_thread(relay, 0.1)


def test_user_added():
    relay = TCPRelay(9975, "0.0.0.0", 9976)
    new_user = "0.0.0.1"
    relay.on_user_connected(new_user)

    users = relay.relay_users()
    assert len(users) == 1
    assert users[0].address == new_user


def test_user_not_removed_on_disconnect():
    # A user should only be disconnected when they send a disconnect request
    relay = TCPRelay(9975, "0.0.0.0", 9976)
    new_user = "0.0.0.1"
    relay.on_user_connected(new_user)
    relay.on_user_disconnected(new_user)

    users = relay.relay_users()
    assert len(users) == 1


def test_user_removed_on_request():
    relay = TCPRelay(9975, "0.0.0.0", 9976)
    new_user = "0.0.0.1"
    relay.on_user_connected(new_user)
    relay.on_user_data_received(b"-", "0.0.0.1")

    users = relay.relay_users()
    assert len(users) == 0
