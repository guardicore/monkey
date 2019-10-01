from time import time


class TestTimer(object):
    def __init__(self, timeout):
        self.timeout_time = TestTimer.get_timeout_time(timeout)
        self.start_time = time()

    def is_timed_out(self):
        return time() > self.timeout_time

    def get_time_taken(self):
        return time() - self.start_time

    @staticmethod
    def get_timeout_time(timeout):
        return time() + timeout
