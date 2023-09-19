from typing import Any, Self, TypeAlias

from pydantic import NonNegativeFloat as PydanticNonNegativeFloat

NonNegativeFloat: TypeAlias = PydanticNonNegativeFloat


class Percent(NonNegativeFloat):
    """
    A type representing a percentage

    Note that percentages can be greater than 100. For example, I may have consumed 120% of my quota
    (if quotas aren't strictly enforced).
    """

    # This __init__() is required so that instances of Percent can be created. If you try to create
    # an instance of NonNegativeFloat, no validation is performed.
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

        # This is required so that floats passed into pydantic models are converted to instances of
        # Percent objects.
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


class PercentLimited(Percent):
    """
    A type representing a percentage limited to 100
    """

    le = 100

    def __init__(self, v: Any):
        PercentLimited._validate_range(v)

    @classmethod
    def __get_validators__(cls):
        for v in super().__get_validators__():
            yield v

    @staticmethod
    def _validate_range(v: Any):
        if not (0.0 <= v <= 100.0):
            raise ValueError("value must be between 0 and 100")
