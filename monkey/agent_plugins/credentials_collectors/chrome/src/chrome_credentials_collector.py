import time
from typing import Sequence

from common.agent_events import CredentialsStolenEvent
from common.credentials import Credentials
from common.event_queue import IAgentEventPublisher
from common.tags import (
    CREDENTIALS_FROM_PASSWORD_STORES_T1555_TAG,
    DATA_FROM_LOCAL_SYSTEM_T1005_TAG,
    UNSECURED_CREDENTIALS_T1552_TAG,
)
from common.types import AgentID, Event

from .typedef import CredentialsDatabaseProcessorCallable, CredentialsDatabaseSelectorCallable

CHROME_CREDETIALS_COLLECTOR_TAG = "chrome-credentials-collector"
CHROME_COLLECTOR_EVENT_TAGS = frozenset(
    (
        CHROME_CREDETIALS_COLLECTOR_TAG,
        DATA_FROM_LOCAL_SYSTEM_T1005_TAG,
        UNSECURED_CREDENTIALS_T1552_TAG,
        CREDENTIALS_FROM_PASSWORD_STORES_T1555_TAG,
    )
)


class ChromeCredentialsCollector:
    def __init__(
        self,
        agent_id: AgentID,
        agent_event_publisher: IAgentEventPublisher,
        select_credentials_database: CredentialsDatabaseSelectorCallable,
        process_credentials_database: CredentialsDatabaseProcessorCallable,
    ):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher
        self._select_credentials_database = select_credentials_database
        self._process_credentials_database = process_credentials_database

    def run(self, interrupt: Event) -> Sequence[Credentials]:
        timestamp = time.time()
        database_paths = self._select_credentials_database()
        credentials = self._process_credentials_database(interrupt, database_paths)

        if len(database_paths) > 0:
            self._publish_credentials_stolen_event(timestamp, credentials)

        return credentials

    def _publish_credentials_stolen_event(
        self,
        timestamp: float,
        collected_credentials: Sequence[Credentials],
    ):
        credentials_stolen_event = CredentialsStolenEvent(
            timestamp=timestamp,
            source=self._agent_id,
            tags=CHROME_COLLECTOR_EVENT_TAGS,
            stolen_credentials=collected_credentials,
        )

        self._agent_event_publisher.publish(credentials_stolen_event)
