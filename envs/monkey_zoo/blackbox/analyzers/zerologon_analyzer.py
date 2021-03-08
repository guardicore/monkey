from typing import List

import dpath.util

from common.config_value_paths import USER_LIST_PATH, PASSWORD_LIST_PATH, NTLM_HASH_LIST_PATH, LM_HASH_LIST_PATH
from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.analyzers.analyzer_log import AnalyzerLog
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient

# Query for telemetry collection to see if password restoration was successful
TELEM_QUERY = {'telem_category': 'exploit',
               'data.exploiter': 'ZerologonExploiter',
               'data.info.password_restored': True}


class ZeroLogonAnalyzer(Analyzer):

    def __init__(self, island_client: MonkeyIslandClient, expected_credentials: List[str]):
        self.island_client = island_client
        self.expected_credentials = expected_credentials
        self.log = AnalyzerLog(self.__class__.__name__)

    def analyze_test_results(self):
        self.log.clear()
        return self._analyze_credential_gathering() and self._analyze_credential_restore()

    def _analyze_credential_gathering(self) -> bool:
        credentials_on_island = []
        config = self.island_client.get_config()
        credentials_on_island.extend(dpath.util.get(config['configuration'], USER_LIST_PATH))
        credentials_on_island.extend(dpath.util.get(config['configuration'], NTLM_HASH_LIST_PATH))
        credentials_on_island.extend(dpath.util.get(config['configuration'], LM_HASH_LIST_PATH))
        return ZeroLogonAnalyzer._is_all_credentials_in_list(self.expected_credentials,
                                                             credentials_on_island)

    @staticmethod
    def _is_all_credentials_in_list(expected_creds: List[str],
                                    all_creds: List[str]) -> bool:
        return all((cred in all_creds) for cred in expected_creds)

    def _analyze_credential_restore(self) -> bool:
        return bool(self.island_client.find_telems_in_db(TELEM_QUERY))
