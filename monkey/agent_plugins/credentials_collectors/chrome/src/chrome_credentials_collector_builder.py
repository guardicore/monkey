import logging

from common import OperatingSystem
from common.event_queue import IAgentEventPublisher
from common.types import AgentID
from infection_monkey.i_puppet import TargetHost

from .chrome_credentials_collector import ChromeCredentialsCollector
from .linux_credentials_database_processor import LinuxCredentialsDatabaseProcessor
from .linux_credentials_database_selector import LinuxCredentialsDatabaseSelector
from .typedef import CredentialsDatabaseProcessorCallable, CredentialsDatabaseSelectorCallable
from .windows_credentials_database_processor import WindowsCredentialsDatabaseProcessor
from .windows_credentials_database_selector import WindowsCredentialsDatabaseSelector

logger = logging.getLogger(__name__)


def build_chrome_credentials_collector(
    host: TargetHost,
    agent_id: AgentID,
    agent_event_publisher: IAgentEventPublisher,
):
    credentials_database_selector = _build_credentials_database_selector(host)
    credentials_database_processor = _build_credentials_database_processor(host)

    return ChromeCredentialsCollector(
        credentials_database_selector,
        credentials_database_processor,
        agent_id,
        agent_event_publisher,
    )


def _build_credentials_database_selector(host: TargetHost) -> CredentialsDatabaseSelectorCallable:
    if host.operating_system == OperatingSystem.WINDOWS:
        return WindowsCredentialsDatabaseSelector()
    return LinuxCredentialsDatabaseSelector()


def _build_credentials_database_processor(host: TargetHost) -> CredentialsDatabaseProcessorCallable:
    if host.operating_system == OperatingSystem.WINDOWS:
        return WindowsCredentialsDatabaseProcessor()
    return LinuxCredentialsDatabaseProcessor()
