import pytest

from common.types import IntRange

INPUTS = [(100, 200), (-200, 100)]


@pytest.mark.parametrize("min,max", INPUTS)
def test_int_range__min_max(min: int, max: int):
    range = IntRange(min, max)
    assert range.min == min
    assert range.max == max


@pytest.mark.parametrize("min,max", INPUTS)
def test_int_range__min_max_reversed(min: int, max: int):
    range = IntRange(max, min)
    assert range.min == min
    assert range.max == max
