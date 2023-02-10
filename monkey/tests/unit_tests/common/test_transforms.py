from itertools import zip_longest
from typing import MutableSequence, Sequence

import pytest

from common.transforms import make_immutable_nested_sequence, make_immutable_sequence


def test_make_immutable_sequence__list():
    mutable_sequence = [1, 2, 3]
    immutable_sequence = make_immutable_sequence(mutable_sequence)

    assert isinstance(immutable_sequence, Sequence)
    assert not isinstance(immutable_sequence, MutableSequence)
    assert_sequences_equal(mutable_sequence, immutable_sequence)


@pytest.mark.parametrize(
    "mutable_sequence",
    [
        [1, 2, 3],
        [[1, 2, 3], [4, 5, 6]],
        [[1, 2, 3, [4, 5, 6]], [4, 5, 6]],
        [8, [5.3, "invalid_comm_type"]],
    ],
)
def test_make_immutable_nested_sequence(mutable_sequence):
    immutable_sequence = make_immutable_nested_sequence(mutable_sequence)

    assert isinstance(immutable_sequence, Sequence)
    assert not isinstance(immutable_sequence, MutableSequence)
    assert_sequences_equal(mutable_sequence, immutable_sequence)


def assert_sequence_immutable_recursive(sequence: Sequence):
    assert not isinstance(sequence, MutableSequence)

    for s in sequence:
        if isinstance(s, str):
            continue

        if isinstance(s, Sequence):
            assert_sequence_immutable_recursive(s)
            assert not isinstance(s, MutableSequence)


def assert_sequences_equal(a: Sequence, b: Sequence):
    assert len(a) == len(b)
    for i, j in zip_longest(a, b):
        if isinstance(i, str) or not isinstance(i, Sequence):
            assert i == j
        else:
            assert_sequences_equal(i, j)
