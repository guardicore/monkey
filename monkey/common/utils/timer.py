import time
from warnings import warn


# TODO: Use EggTimer
class Timer:
    """
    A class for checking whether or not a certain amount of time has elapsed.
    """

    def __init__(self):
        warn("Timer is deprecated. EggTimer instead.", DeprecationWarning, stacklevel=2)
        self._timeout_sec = 0
        self._start_time = 0

    def set(self, timeout_sec: float):
        """
        Set a timer

        :param float timeout_sec: A nonnegative floating point number expressing the number of
                                  seconds to set the timeout for.
        """
        self._timeout_sec = timeout_sec
        self._start_time = time.time()

    def is_expired(self):
        """
        Check whether or not the timer has expired

        :return: True if the elapsed time since set(TIMEOUT_SEC) was called is greater than
                 TIMEOUT_SEC, False otherwise
        :rtype: bool
        """
        return self.time_remaining == 0

    @property
    def time_remaining(self) -> float:
        """
        Return the amount of time remaining until the timer expires.

        :return: The number of seconds until the timer expires. If the timer is expired, this
                 function returns 0 (it will never return a negative number).
        :rtype: float
        """
        time_remaining = self._timeout_sec - (time.time() - self._start_time)
        return max(time_remaining, 0)

    def reset(self):
        """
        Reset the timer without changing the timeout
        """
        self._start_time = time.time()
