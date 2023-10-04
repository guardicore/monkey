import logging

from monkeytypes import OperatingSystem

from common.event_queue import IAgentEventPublisher
from common.types import AgentID
from common.utils.environment import get_os

from .chrome_credentials_collector import ChromeCredentialsCollector
from .database_reader import get_credentials_from_database
from .typedef import CredentialsDatabaseProcessorCallable, CredentialsDatabaseSelectorCallable

logger = logging.getLogger(__name__)


def build_chrome_credentials_collector(
    agent_id: AgentID,
    agent_event_publisher: IAgentEventPublisher,
):
    credentials_database_selector = _build_credentials_database_selector()
    credentials_database_processor = _build_credentials_database_processor()

    return ChromeCredentialsCollector(
        agent_id,
        agent_event_publisher,
        credentials_database_selector,
        credentials_database_processor,
    )


def _build_credentials_database_selector() -> CredentialsDatabaseSelectorCallable:
    if get_os() == OperatingSystem.WINDOWS:
        from .windows_credentials_database_selector import WindowsCredentialsDatabaseSelector

        return WindowsCredentialsDatabaseSelector()

    from .linux_credentials_database_selector import LinuxCredentialsDatabaseSelector

    return LinuxCredentialsDatabaseSelector()


def _build_credentials_database_processor() -> CredentialsDatabaseProcessorCallable:
    if get_os() == OperatingSystem.WINDOWS:
        from .windows_credentials_database_processor import WindowsCredentialsDatabaseProcessor

        return WindowsCredentialsDatabaseProcessor(get_credentials_from_database)

    from .linux_credentials_database_processor import LinuxCredentialsDatabaseProcessor

    return LinuxCredentialsDatabaseProcessor(get_credentials_from_database)
