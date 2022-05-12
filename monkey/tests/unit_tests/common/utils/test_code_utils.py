from queue import Queue

from common.utils.code_utils import queue_to_list


def test_empty_queue_to_empty_list():
    q = Queue()

    list_ = queue_to_list(q)

    assert len(list_) == 0


def test_queue_to_list():
    expected_list = [8, 6, 7, 5, 3, 0, 9]
    q = Queue()
    for i in expected_list:
        q.put(i)

    list_ = queue_to_list(q)

    assert list_ == expected_list
