import logging

from agentpluginapi import IAgentEventPublisher
from monkeytypes import AgentID, OperatingSystem

from .chrome_credentials_collector import ChromeCredentialsCollector
from .database_reader import get_credentials_from_database
from .typedef import CredentialsDatabaseProcessorCallable, CredentialsDatabaseSelectorCallable

logger = logging.getLogger(__name__)


def build_chrome_credentials_collector(
    agent_id: AgentID,
    agent_event_publisher: IAgentEventPublisher,
    operating_system: OperatingSystem,
):
    credentials_database_selector = _build_credentials_database_selector(operating_system)
    credentials_database_processor = _build_credentials_database_processor(operating_system)

    return ChromeCredentialsCollector(
        agent_id,
        agent_event_publisher,
        credentials_database_selector,
        credentials_database_processor,
    )


def _build_credentials_database_selector(
    operating_system: OperatingSystem,
) -> CredentialsDatabaseSelectorCallable:
    if operating_system == OperatingSystem.WINDOWS:
        from .windows_credentials_database_selector import WindowsCredentialsDatabaseSelector

        return WindowsCredentialsDatabaseSelector()

    from .linux_credentials_database_selector import LinuxCredentialsDatabaseSelector

    return LinuxCredentialsDatabaseSelector()


def _build_credentials_database_processor(
    operating_system: OperatingSystem,
) -> CredentialsDatabaseProcessorCallable:
    if operating_system == OperatingSystem.WINDOWS:
        from .windows_credentials_database_processor import WindowsCredentialsDatabaseProcessor

        return WindowsCredentialsDatabaseProcessor(get_credentials_from_database)

    from .linux_credentials_database_processor import LinuxCredentialsDatabaseProcessor

    return LinuxCredentialsDatabaseProcessor(get_credentials_from_database)
