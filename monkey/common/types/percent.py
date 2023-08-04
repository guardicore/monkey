from typing import Any, Self

from pydantic import NonNegativeFloat


class Percent(NonNegativeFloat):
    """
    A type representing a percentage

    Note that percentages can be greater than 100. For example, I may have consumed 120% of my quota
    (if quotas aren't strictly enforced).
    """

    def __init__(self, v: Any):
        Percent._validate_range(v)

    @classmethod
    def __get_validators__(cls):
        for v in super().__get_validators__():
            yield v

        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> Self:
        cls._validate_range(v)

        return cls(v)

    @staticmethod
    def _validate_range(v: Any):
        if v < 0:
            raise ValueError("value must be non-negative")

    def as_decimal_fraction(self) -> NonNegativeFloat:
        """
        Return the percentage as a decimal fraction

        Example: 50% -> 0.5

        return: The percentage as a decimal fraction
        """
        return self / 100.0
