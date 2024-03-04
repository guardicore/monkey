from pathlib import PurePath
from unittest.mock import MagicMock

import pytest
from agent_plugins.credentials_collectors.chrome.src.chrome_credentials_collector import (
    ChromeCredentialsCollector,
)
from agent_plugins.credentials_collectors.chrome.src.typedef import (
    CredentialsDatabaseProcessorCallable,
    CredentialsDatabaseSelectorCallable,
)
from agentpluginapi import IAgentEventPublisher
from monkeytypes import AgentID
from tests.data_for_tests.propagation_credentials import CREDENTIALS

AGENT_ID = AgentID("43b1dabd-27e3-4c13-9c2d-fc870f7266cc")
DATABASE_PATHS = [PurePath("some_path"), PurePath("some_other_path")]


@pytest.fixture
def event_publisher():
    return MagicMock(spec=IAgentEventPublisher)


@pytest.fixture
def database_selector():
    return MagicMock(spec=CredentialsDatabaseSelectorCallable, return_value=DATABASE_PATHS)


@pytest.fixture
def database_processor():
    return MagicMock(spec=CredentialsDatabaseProcessorCallable, return_value=CREDENTIALS)


@pytest.fixture
def chrome_credentials_collector(event_publisher, database_selector, database_processor):
    return ChromeCredentialsCollector(
        agent_id=AGENT_ID,
        agent_event_publisher=event_publisher,
        select_credentials_database=database_selector,
        process_credentials_database=database_processor,
    )


def test_run__returns_empty_list_if_no_credentials_found(
    chrome_credentials_collector, database_processor
):
    database_processor.return_value = []
    actual_credentials = chrome_credentials_collector.run(interrupt=MagicMock())

    assert actual_credentials == []


def test_run__returns_credentials_if_found(chrome_credentials_collector):
    actual_credentials = chrome_credentials_collector.run(interrupt=MagicMock())

    assert actual_credentials == CREDENTIALS


def test_run__publishes_credentials_stolen_event_if_no_credentials_found(
    chrome_credentials_collector, event_publisher, database_processor
):
    database_processor.return_value = []
    chrome_credentials_collector.run(interrupt=MagicMock())

    event_publisher.publish.assert_called_once()
    event = event_publisher.publish.call_args_list[0][0][0]
    assert event.source == AGENT_ID
    assert event.stolen_credentials == []


def test_run__does_not_publish_credentials_stolen_event_if_no_databases_found(
    chrome_credentials_collector, event_publisher, database_selector
):
    database_selector.return_value = []
    chrome_credentials_collector.run(interrupt=MagicMock())

    event_publisher.publish.assert_not_called()


def test_run__publishes_credentials_stolen_event_with_discovered_credentials(
    chrome_credentials_collector, event_publisher
):
    chrome_credentials_collector.run(interrupt=MagicMock())

    event_publisher.publish.assert_called_once()
    event = event_publisher.publish.call_args_list[0][0][0]
    assert event.source == AGENT_ID
    assert event.stolen_credentials == CREDENTIALS
