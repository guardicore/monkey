import logging
from threading import Event, current_thread

from infection_monkey.utils.threading import (
    create_daemon_thread,
    interruptable_iter,
    run_worker_threads,
)


def test_create_daemon_thread():
    thread = create_daemon_thread(lambda: None)
    assert thread.daemon


def test_create_daemon_thread_naming():
    thread = create_daemon_thread(lambda: None, name="test")
    assert thread.name == "test"


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


def test_worker_thread_names():
    thread_names = set()

    def add_thread_name_to_list():
        thread_names.add(current_thread().name)

    run_worker_threads(target=add_thread_name_to_list, name_prefix="A", num_workers=2)
    run_worker_threads(target=add_thread_name_to_list, name_prefix="B", num_workers=2)
    run_worker_threads(target=add_thread_name_to_list, name_prefix="A", num_workers=2)

    assert "A-1" in thread_names
    assert "A-2" in thread_names
    assert "A-3" in thread_names
    assert "A-4" in thread_names
    assert "B-1" in thread_names
    assert "B-2" in thread_names
    assert len(thread_names) == 6
