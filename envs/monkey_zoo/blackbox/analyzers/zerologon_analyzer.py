from typing import List

from monkeytypes import Credentials, LMHash, NTHash, Username

from common.agent_event_serializers import EVENT_TYPE_FIELD
from common.agent_events import PasswordRestorationEvent
from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.analyzers.analyzer_log import AnalyzerLog
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient


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
            if isinstance(credentials.identity, Username):
                credentials_on_island.update([credentials.identity.username])
            if isinstance(credentials.secret, NTHash):
                credentials_on_island.update([credentials.secret.nt_hash.get_secret_value()])
            if isinstance(credentials.secret, LMHash):
                credentials_on_island.update([credentials.secret.lm_hash.get_secret_value()])

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
        agent_events = self.island_client.get_agent_events()
        password_restoration_events = (
            event
            for event in agent_events
            if event[EVENT_TYPE_FIELD] == PasswordRestorationEvent.__name__
        )

        _password_restored = any((event["success"] for event in password_restoration_events))

        self._log_credential_restore(_password_restored)
        return _password_restored

    def _log_credential_restore(self, password_restored: bool):
        if password_restored:
            self.log.add_entry(
                "Zerologon exploiter events indicate that credentials "
                "were successfully restored."
            )
        else:
            self.log.add_entry(
                "Credential restore failed or credential restore events were not sent."
            )
