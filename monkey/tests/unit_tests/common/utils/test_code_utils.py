from queue import Queue

import pytest

from common.utils.code_utils import del_key, insecure_generate_random_string, queue_to_list


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
    assert key_to_delete in my_dict

    del_key(my_dict, key_to_delete)
    assert key_to_delete not in my_dict

    # This test passes if the following call does not raise an error
    del_key(my_dict, key_to_delete)
    assert key_to_delete not in my_dict


def test_insecure_generate_random_string__random_value():
    assert insecure_generate_random_string(n=5) != insecure_generate_random_string(n=5)


@pytest.mark.parametrize("length", [1, 2, 4, 8, 16, 32])
def test_insecure_generate_random_string__str_length(length):
    assert len(insecure_generate_random_string(n=length)) == length


def test_insecure_generate_random_string__invalid_length_type():
    with pytest.raises(TypeError):
        insecure_generate_random_string(n="string")


def test_character_set():
    character_set = "abcde"
    n = len(character_set) * 5

    random_str = insecure_generate_random_string(n=n, character_set=character_set)

    for c in random_str:
        assert c in character_set
