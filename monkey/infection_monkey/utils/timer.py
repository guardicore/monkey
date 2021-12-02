import time


class Timer:
    """
    A class for checking whether or not a certain amount of time has elapsed.
    """

    def __init__(self):
        self._timeout_sec = 0
        self._start_time = 0

    def set(self, timeout_sec: float):
        """
        Set a timer
        :param float timeout_sec: A fractional number of seconds to set the timeout for.
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
        return (time.time() - self._start_time) >= self._timeout_sec

    def reset(self):
        """
        Reset the timer without changing the timeout
        """
        self._start_time = time.time()
