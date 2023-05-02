from typing import List, Sequence

from common.credentials import Credentials
from common.credentials.encoding import get_plaintext
from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.analyzers.analyzer_log import AnalyzerLog
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient


class MimikatzAnalyzer(Analyzer):
    def __init__(self, island_client: MonkeyIslandClient, expected_stolen_credentials: List[str]):
        self.island_client = island_client
        self.expected_stolen_credentials = expected_stolen_credentials

        self.log = AnalyzerLog(self.__class__.__name__)

    def analyze_test_results(self) -> bool:
        self.log.clear()

        credential_stealing_success = self._analyze_credential_stealing()

        return credential_stealing_success

    def _analyze_credential_stealing(self) -> bool:
        stolen_credentials = self.island_client.get_stolen_credentials()
        plaintext_stolen_credentials = MimikatzAnalyzer._get_plaintext_stolen_credentials(
            stolen_credentials
        )

        return self._all_expected_credentials_stolen(plaintext_stolen_credentials)

    @staticmethod
    def _get_plaintext_stolen_credentials(stolen_credentials: Sequence[Credentials]) -> List[str]:
        plaintext_stolen_credentials = set()

        for credentials in stolen_credentials:
            if credentials.identity:
                plaintext_stolen_credentials.add(credentials.identity.username)
            if credentials.secret:
                # example of what the variables here look like:
                #     credentials.secret = Password(password=SecretStr("abc")))
                #     secret_tuple = ('password', SecretStr("abc"))
                for secret_tuple in credentials.secret:
                    plaintext_stolen_credentials.add(get_plaintext(secret_tuple[1]))

        return list(plaintext_stolen_credentials)

    def _all_expected_credentials_stolen(self, stolen_credentials: List[str]) -> bool:
        missing_credentials = [
            credential
            for credential in self.expected_stolen_credentials
            if credential not in stolen_credentials
        ]
        self._log_missing_credentials(missing_credentials)

        return len(missing_credentials) == 0

    def _log_missing_credentials(self, missing_credentials: List[str]):
        if not missing_credentials:
            self.log.add_entry("Mimikatz stole all expected credentials")
        else:
            for credential in missing_credentials:
                self.log.add_entry(f"Mimikatz did not steal expected credential: {credential}")
