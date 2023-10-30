import pytest
from monkeytypes import PercentLimited
from pydantic import BaseModel

from common.types import Percent


class Model(BaseModel):
    p: Percent


def test_non_negative_percent():
    with pytest.raises(ValueError):
        Percent(-1.0)


def test_incorrect_type():
    with pytest.raises(ValueError):
        Percent("stuff")


@pytest.mark.parametrize("input_value", [0.0, 1.0, 99.9, 100.0, 120.5, 50.123, 25])
def test_valid_percent(input_value: float):
    assert Percent(input_value) == input_value  # type: ignore [arg-type]


@pytest.mark.parametrize(
    "input_value,expected_decimal_fraction",
    [(0.0, 0.0), (99, 0.99), (51.234, 0.51234), (121.2, 1.212)],
)
def test_as_decimal_fraction(input_value: float, expected_decimal_fraction: float):
    assert Model(p=input_value).p.as_decimal_fraction() == expected_decimal_fraction  # type: ignore [arg-type]  # noqa: E501


class ModelLimited(BaseModel):
    p: PercentLimited


@pytest.mark.parametrize("input_value", (-1, -0.01, 100.01))
def test_percent_limited_out_of_range(input_value: float):
    with pytest.raises(ValueError):
        PercentLimited(input_value)


@pytest.mark.parametrize("input_value", [0.0, 1.0, 99.9, 100.0, 50.123, 25])
def test_valid_percent_limited(input_value: float):
    assert PercentLimited(input_value) == input_value  # type: ignore [arg-type]


@pytest.mark.parametrize(
    "input_value,expected_decimal_fraction", [(0.0, 0.0), (99, 0.99), (51.234, 0.51234)]
)
def test_as_decimal_fraction_limited(input_value: float, expected_decimal_fraction: float):
    assert ModelLimited(p=input_value).p.as_decimal_fraction() == expected_decimal_fraction  # type: ignore [arg-type]  # noqa: E501
