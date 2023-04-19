class IntRange:
    """
    Represents a range of integers, with a step size of 1.

    Ensures that min <= max.
    """

    def __init__(self, a: int, b: int):
        self._min = a
        self._max = b
        if a > b:
            self._min, self._max = b, a

    @property
    def max(self) -> int:
        """The maximum value in the range."""
        return self._max

    @property
    def min(self) -> int:
        """The minimum value in the range."""
        return self._min
