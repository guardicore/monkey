import logging
from itertools import zip_longest
from threading import Event, current_thread
from typing import Any

from infection_monkey.utils.threading import (
    ThreadSafeIterator,
    create_daemon_thread,
    interruptible_function,
    interruptible_iter,
    run_worker_threads,
)


def test_create_daemon_thread():
    thread = create_daemon_thread(lambda: None, name="test")
    assert thread.daemon


def test_create_daemon_thread_naming():
    thread = create_daemon_thread(lambda: None, name="test")
    assert thread.name == "test"


def test_interruptible_iter():
    interrupt = Event()
    items_from_iterator = []
    test_iterator = interruptible_iter(range(0, 10), interrupt, "Test iterator was interrupted")

    for i in test_iterator:
        items_from_iterator.append(i)
        if i == 3:
            interrupt.set()

    assert items_from_iterator == [0, 1, 2, 3]


def test_interruptible_iter_not_interrupted():
    interrupt = Event()
    items_from_iterator = []
    test_iterator = interruptible_iter(range(0, 5), interrupt, "Test iterator was interrupted")

    for i in test_iterator:
        items_from_iterator.append(i)

    assert items_from_iterator == [0, 1, 2, 3, 4]


def test_interruptible_iter_interrupted_before_used():
    interrupt = Event()
    items_from_iterator = []
    test_iterator = interruptible_iter(
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

    assert "A-01" in thread_names
    assert "A-02" in thread_names
    assert "A-03" in thread_names
    assert "A-04" in thread_names
    assert "B-01" in thread_names
    assert "B-02" in thread_names
    assert len(thread_names) == 6


class MockFunction:
    def __init__(self):
        self._call_count = 0

    @property
    def call_count(self):
        return self._call_count

    @property
    def return_value(self):
        return 42

    def __call__(self, *_, interrupt: Event) -> Any:
        self._call_count += 1

        return self.return_value


def test_interruptible_decorator_calls_decorated_function():
    fn = MockFunction()
    int_fn = interruptible_function()(fn)

    return_value = int_fn(interrupt=Event())

    assert return_value == fn.return_value
    assert fn.call_count == 1


def test_interruptible_decorator_skips_decorated_function():
    fn = MockFunction()
    int_fn = interruptible_function()(fn)
    interrupt = Event()
    interrupt.set()

    return_value = int_fn(interrupt=interrupt)

    assert return_value is None
    assert fn.call_count == 0


def test_interruptible_decorator_returns_default_value_on_interrupt():
    fn = MockFunction()
    int_fn = interruptible_function(default_return_value=777)(fn)
    interrupt = Event()
    interrupt.set()

    return_value = int_fn(interrupt=interrupt)

    assert return_value == 777
    assert fn.call_count == 0


def test_thread_safe_iterator():
    test_list = [1, 2, 3, 4, 5]
    tsi = ThreadSafeIterator(test_list.__iter__())

    for actual, expected in zip_longest(tsi, test_list):
        assert actual == expected
