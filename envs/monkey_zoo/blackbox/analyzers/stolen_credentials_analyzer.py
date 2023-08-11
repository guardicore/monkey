from typing import Set

from common.credentials import Credentials
from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.analyzers.analyzer_log import AnalyzerLog
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient


class StolenCredentialsAnalyzer(Analyzer):
    def __init__(
        self, island_client: MonkeyIslandClient, expected_stolen_credentials: Set[Credentials]
    ):
        self.island_client = island_client
        self.expected_stolen_credentials = set(expected_stolen_credentials)

        self.log = AnalyzerLog(self.__class__.__name__)

    def analyze_test_results(self) -> bool:
        self.log.clear()

        stolen_credentials = set(self.island_client.get_stolen_credentials())

        if set(self.expected_stolen_credentials).issubset(stolen_credentials):
            self.log.add_entry("All expected credentials were stolen")
            return True

        missing = set(self.expected_stolen_credentials) - set(stolen_credentials)
        self.log.add_entry(f"Some credentials were not stolen: {list(missing)}")

        return False
