from infection_monkey.master.threading_utils import create_daemon_thread


def test_create_daemon_thread():
    thread = create_daemon_thread(lambda: None)
    assert thread.daemon
