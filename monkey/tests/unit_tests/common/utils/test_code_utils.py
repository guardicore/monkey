from queue import Queue
from typing import Callable

import pytest

from common.utils.code_utils import (
    apply_filters,
    del_key,
    insecure_generate_random_string,
    queue_to_list,
    secure_generate_random_string,
)


def test_apply_filters():
    iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    filters = [lambda x: x % 2 == 0, lambda x: x > 2, lambda x: x != 6]

    filtered_iterable = apply_filters(filters, iterable)

    assert list(filtered_iterable) == [4, 8, 10, 12, 14]


def test_apply_filters__no_filters_provided():
    iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    filtered_iterable = apply_filters([], iterable)

    assert list(filtered_iterable) == iterable


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


@pytest.mark.parametrize(
    "generate_random_string", [insecure_generate_random_string, secure_generate_random_string]
)
@pytest.mark.parametrize("n", [2, 4, 8, 16, 32])
def test_generate_random_string__random_value(generate_random_string: Callable[..., str], n):
    assert generate_random_string(n=n) != generate_random_string(n=n)


@pytest.mark.parametrize(
    "generate_random_string", [insecure_generate_random_string, secure_generate_random_string]
)
@pytest.mark.parametrize("n", [2, 4, 8, 16, 32])
def test_generate_random_string__str_length(generate_random_string: Callable[..., str], n: int):
    assert len(generate_random_string(n=n)) == n


@pytest.mark.parametrize(
    "generate_random_string", [insecure_generate_random_string, secure_generate_random_string]
)
def test_generate_random_string__invalid_length_type(generate_random_string: Callable[..., str]):
    with pytest.raises(TypeError):
        generate_random_string(n="string")


def test_character_set():
    character_set = "abcde"
    n = len(character_set) * 5

    random_str = insecure_generate_random_string(n=n, character_set=character_set)

    for c in random_str:
        assert c in character_set
