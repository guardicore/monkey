import logging
from threading import Event

from infection_monkey.master.threading_utils import create_daemon_thread, interruptable_iter


def test_create_daemon_thread():
    thread = create_daemon_thread(lambda: None)
    assert thread.daemon


def test_interruptable_iter():
    interrupt = Event()
    items_from_iterator = []
    test_iterator = interruptable_iter(range(0, 10), interrupt, "Test iterator was interrupted")

    for i in test_iterator:
        items_from_iterator.append(i)
        if i == 3:
            interrupt.set()

    assert items_from_iterator == [0, 1, 2, 3]


def test_interruptable_iter_not_interrupted():
    interrupt = Event()
    items_from_iterator = []
    test_iterator = interruptable_iter(range(0, 5), interrupt, "Test iterator was interrupted")

    for i in test_iterator:
        items_from_iterator.append(i)

    assert items_from_iterator == [0, 1, 2, 3, 4]


def test_interruptable_iter_interrupted_before_used():
    interrupt = Event()
    items_from_iterator = []
    test_iterator = interruptable_iter(
        range(0, 5), interrupt, "Test iterator was interrupted", logging.INFO
    )

    interrupt.set()
    for i in test_iterator:
        items_from_iterator.append(i)

    assert not items_from_iterator
