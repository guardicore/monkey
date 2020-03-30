import logging
from datetime import timedelta

from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient

MAX_ALLOWED_SINGLE_PAGE_TIME = timedelta(seconds=2)
MAX_ALLOWED_TOTAL_TIME = timedelta(seconds=5)

REPORT_URLS = [
    "api/report/security",
    "api/attack/report",
    "api/report/zero_trust/findings",
    "api/report/zero_trust/principles",
    "api/report/zero_trust/pillars"
]

LOGGER = logging.getLogger(__name__)


class PerformanceAnalyzer(Analyzer):

    def __init__(self, island_client: MonkeyIslandClient, break_if_took_too_long=False):
        self.break_if_took_too_long = break_if_took_too_long
        self.island_client = island_client



    def get_elapsed_for_get_request(self, url):
        response = self.island_client.requests.get(url)
        if response.ok:
            LOGGER.debug(f"Got ok for {url} content peek:\n{response.content[:120].strip()}")
            return response.elapsed
        else:
            LOGGER.error(f"Trying to get {url} but got unexpected {str(response)}")
            # instead of raising for status, mark failed responses as maxtime
            return timedelta.max()
