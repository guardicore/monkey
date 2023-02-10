from typing import Any, MutableSequence, Sequence, Union


def make_immutable_nested_sequence(sequence_or_element: Union[Sequence, Any]) -> Sequence:
    """
    Take a Sequence of Sequences (or other types) and return an immutable copy

    Takes a Sequence of Sequences, for example `List[List[int, float]]]` and returns an immutable
    copy. Note that if the Sequence does not contain other sequences, `make_sequence_immutable()`
    will be more performant.

    :param sequence_or_element: A nested sequence or an element from within a nested sequence
    :return: An immutable copy of the sequence if `sequence_or_element` is a Sequence, otherwise
             just return `sequence_or_element`
    """
    if isinstance(sequence_or_element, str):
        return sequence_or_element

    if isinstance(sequence_or_element, Sequence):
        return tuple(map(make_immutable_nested_sequence, sequence_or_element))

    return sequence_or_element


def make_immutable_sequence(sequence: Sequence):
    """
    Take a Sequence and return an immutable copy

    :param sequence: A Sequence to create an immutable copy from
    :return: An immutable copy of `sequence`
    """

    if isinstance(sequence, MutableSequence):
        return tuple(sequence)

    return sequence
