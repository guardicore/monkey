from pprint import pformat
from typing import List

from common.credentials import CredentialComponentType, Credentials
from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.analyzers.analyzer_log import AnalyzerLog
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient

# Query for telemetry collection to see if password restoration was successful
TELEM_QUERY = {
    "telem_category": "exploit",
    "data.exploiter": "ZerologonExploiter",
    "data.info.password_restored": True,
}


class ZerologonAnalyzer(Analyzer):
    def __init__(self, island_client: MonkeyIslandClient, expected_credentials: List[str]):
        self.island_client = island_client
        self.expected_credentials = expected_credentials
        self.log = AnalyzerLog(self.__class__.__name__)

    def analyze_test_results(self):
        self.log.clear()
        is_creds_gathered = self._analyze_credential_gathering()
        is_creds_restored = self._analyze_credential_restore()
        return is_creds_gathered and is_creds_restored

    def _analyze_credential_gathering(self) -> bool:
        propagation_credentials = self.island_client.get_propagation_credentials()
        credentials_on_island = ZerologonAnalyzer._get_relevant_credentials(propagation_credentials)
        return self._is_all_credentials_in_list(credentials_on_island)

    @staticmethod
    def _get_relevant_credentials(propagation_credentials: Credentials) -> List[str]:
        credentials_on_island = set()

        for credentials in propagation_credentials:
            if credentials.identity.credential_type is CredentialComponentType.USERNAME:
                credentials_on_island.update([credentials.identity.username])
            if credentials.secret.credential_type is CredentialComponentType.NT_HASH:
                credentials_on_island.update([credentials.secret.nt_hash])
            if credentials.secret.credential_type is CredentialComponentType.LM_HASH:
                credentials_on_island.update([credentials.secret.lm_hash])

        return list(credentials_on_island)

    def _is_all_credentials_in_list(self, all_creds: List[str]) -> bool:
        credentials_missing = [cred for cred in self.expected_credentials if cred not in all_creds]
        self._log_creds_not_gathered(credentials_missing)
        return not credentials_missing

    def _log_creds_not_gathered(self, missing_creds: List[str]):
        if not missing_creds:
            self.log.add_entry("Zerologon exploiter gathered all credentials expected.")
        else:
            for cred in missing_creds:
                self.log.add_entry(f"Credential Zerologon exploiter failed to gathered:{cred}.")

    def _analyze_credential_restore(self) -> bool:
        cred_restore_telems = self.island_client.find_telems_in_db(TELEM_QUERY)
        self._log_credential_restore(cred_restore_telems)
        return bool(cred_restore_telems)

    def _log_credential_restore(self, telem_list: List[dict]):
        if telem_list:
            self.log.add_entry(
                "Zerologon exploiter telemetry contains indicators that credentials "
                "were successfully restored."
            )
        else:
            self.log.add_entry(
                "Credential restore failed or credential restore "
                "telemetry not found on the Monkey Island."
            )
            self.log.add_entry(f"Query for credential restore telem: {pformat(TELEM_QUERY)}")
