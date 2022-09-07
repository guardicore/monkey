from queue import Queue

from common.utils.code_utils import del_key, in_sorted_sequence, queue_to_list


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


def test_del_key__deletes_key():
    key_to_delete = "a"
    my_dict = {"a": 1, "b": 2}
    expected_dict = {k: v for k, v in my_dict.items() if k != key_to_delete}

    del_key(my_dict, key_to_delete)

    assert my_dict == expected_dict


def test_del_key__nonexistant_key():
    key_to_delete = "a"
    my_dict = {"a": 1, "b": 2}

    del_key(my_dict, key_to_delete)

    # This test passes if the following call does not raise an error
    del_key(my_dict, key_to_delete)


def test_in_sorted_sequence__finds_item():
    assert in_sorted_sequence(99, range(100))


def test_in_sorted_sequence__does_not_find_nonexistent_item():
    assert not in_sorted_sequence(101, range(100))
