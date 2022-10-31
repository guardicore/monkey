import threading
from pathlib import PurePosixPath
from typing import Type
from unittest.mock import MagicMock

import pytest
from tests.unit_tests.infection_monkey.payload.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    HELLO_TXT,
    TEST_KEYBOARD_TXT,
)

from common.agent_events import AbstractAgentEvent, FileEncryptionEvent
from common.event_queue import AgentEventSubscriber, IAgentEventQueue
from infection_monkey.payload.ransomware.consts import README_FILE_NAME, README_SRC
from infection_monkey.payload.ransomware.ransomware import Ransomware
from infection_monkey.payload.ransomware.ransomware_options import RansomwareOptions


class AgentEventQueueSpy(IAgentEventQueue):
    def __init__(self):
        self.events = []

    def subscribe_all_events(self, subscriber: AgentEventSubscriber):
        pass

    def subscribe_type(
        self, event_type: Type[AbstractAgentEvent], subscriber: AgentEventSubscriber
    ):
        pass

    def subscribe_tag(self, tag: str, subscriber: AgentEventSubscriber):
        pass

    def publish(self, event: AbstractAgentEvent):
        self.events.append(event)


@pytest.fixture
def agent_event_queue_spy():
    return AgentEventQueueSpy()


@pytest.fixture
def ransomware(build_ransomware, ransomware_options):
    return build_ransomware(ransomware_options)


@pytest.fixture
def build_ransomware(
    mock_file_encryptor, mock_file_selector, mock_leave_readme, agent_event_queue_spy
):
    def inner(
        config,
        file_encryptor=mock_file_encryptor,
        file_selector=mock_file_selector,
        leave_readme=mock_leave_readme,
    ):
        return Ransomware(
            config,
            file_encryptor,
            file_selector,
            leave_readme,
            agent_event_queue_spy,
        )

    return inner


@pytest.fixture
def ransomware_options(ransomware_file_extension, ransomware_test_data):
    class RansomwareOptionsStub(RansomwareOptions):
        def __init__(self, encryption_enabled, readme_enabled, file_extension, target_directory):
            self.encryption_enabled = encryption_enabled
            self.readme_enabled = readme_enabled
            self.file_extension = file_extension
            self.target_directory = target_directory

    return RansomwareOptionsStub(True, False, ransomware_file_extension, ransomware_test_data)


@pytest.fixture
def mock_file_encryptor():
    return MagicMock()


@pytest.fixture
def mock_file_selector(ransomware_test_data):
    selected_files = iter(
        [
            ransomware_test_data / ALL_ZEROS_PDF,
            ransomware_test_data / TEST_KEYBOARD_TXT,
        ]
    )
    return MagicMock(return_value=selected_files)


@pytest.fixture
def mock_leave_readme():
    return MagicMock()


@pytest.fixture
def interrupt():
    return threading.Event()


def test_files_selected_from_target_dir(
    ransomware,
    ransomware_options,
    mock_file_selector,
):
    ransomware.run(threading.Event())
    mock_file_selector.assert_called_with(ransomware_options.target_directory)


def test_all_selected_files_encrypted(ransomware_test_data, ransomware, mock_file_encryptor):
    ransomware.run(threading.Event())

    assert mock_file_encryptor.call_count == 2
    mock_file_encryptor.assert_any_call(ransomware_test_data / ALL_ZEROS_PDF)
    mock_file_encryptor.assert_any_call(ransomware_test_data / TEST_KEYBOARD_TXT)


def test_interrupt_while_encrypting(
    ransomware_test_data, interrupt, ransomware_options, build_ransomware
):
    selected_files = [
        ransomware_test_data / ALL_ZEROS_PDF,
        ransomware_test_data / HELLO_TXT,
        ransomware_test_data / TEST_KEYBOARD_TXT,
    ]
    mfs = MagicMock(return_value=selected_files)

    def _callback(file_path, *_):
        # Block all threads here until 2 threads reach this barrier, then set stop
        # and test that neither thread continues to scan.
        if file_path.name == HELLO_TXT:
            interrupt.set()

    mfe = MagicMock(side_effect=_callback)

    build_ransomware(ransomware_options, mfe, mfs).run(interrupt)

    assert mfe.call_count == 2
    mfe.assert_any_call(ransomware_test_data / ALL_ZEROS_PDF)
    mfe.assert_any_call(ransomware_test_data / HELLO_TXT)


def test_no_readme_after_interrupt(
    ransomware_options, build_ransomware, interrupt, mock_leave_readme
):
    ransomware_options.readme_enabled = True
    ransomware = build_ransomware(ransomware_options)

    interrupt.set()
    ransomware.run(interrupt)

    mock_leave_readme.assert_not_called()


def test_encryption_skipped_if_configured_false(
    build_ransomware, ransomware_options, mock_file_encryptor
):
    ransomware_options.encryption_enabled = False

    ransomware = build_ransomware(ransomware_options)
    ransomware.run(threading.Event())

    assert mock_file_encryptor.call_count == 0


def test_encryption_skipped_if_no_directory(
    build_ransomware, ransomware_options, mock_file_encryptor
):
    ransomware_options.encryption_enabled = True
    ransomware_options.target_directory = None

    ransomware = build_ransomware(ransomware_options)
    ransomware.run(threading.Event())

    assert mock_file_encryptor.call_count == 0


def test_readme_false(build_ransomware, ransomware_options, mock_leave_readme):
    ransomware_options.readme_enabled = False
    ransomware = build_ransomware(ransomware_options)

    ransomware.run(threading.Event())
    mock_leave_readme.assert_not_called()


def test_readme_true(build_ransomware, ransomware_options, mock_leave_readme, ransomware_test_data):
    ransomware_options.readme_enabled = True
    ransomware = build_ransomware(ransomware_options)

    ransomware.run(threading.Event())
    mock_leave_readme.assert_called_with(README_SRC, ransomware_test_data / README_FILE_NAME)


def test_no_readme_if_no_directory(build_ransomware, ransomware_options, mock_leave_readme):
    ransomware_options.target_directory = None
    ransomware_options.readme_enabled = True

    ransomware = build_ransomware(ransomware_options)

    ransomware.run(threading.Event())
    mock_leave_readme.assert_not_called()


def test_leave_readme_exceptions_handled(build_ransomware, ransomware_options):
    leave_readme = MagicMock(side_effect=Exception("Test exception when leaving README"))
    ransomware_options.readme_enabled = True
    ransomware = build_ransomware(config=ransomware_options, leave_readme=leave_readme)

    # Test will fail if exception is raised and not handled
    ransomware.run(threading.Event())


def test_file_encryption_event_publishing(
    agent_event_queue_spy, ransomware_test_data, ransomware_options, build_ransomware
):
    expected_selected_files = [
        ransomware_test_data / ALL_ZEROS_PDF,
        ransomware_test_data / HELLO_TXT,
        ransomware_test_data / TEST_KEYBOARD_TXT,
    ]
    mfs = MagicMock(return_value=expected_selected_files)

    build_ransomware(ransomware_options, MagicMock(), mfs).run(threading.Event())

    assert len(agent_event_queue_spy.events) == 3

    for event in agent_event_queue_spy.events:
        assert event.__class__ is FileEncryptionEvent
        assert event.success
        assert event.target is None

    actual_file_paths = [event.file_path for event in agent_event_queue_spy.events]
    assert expected_selected_files == actual_file_paths


def test_file_encryption_event_publishing__failed(
    agent_event_queue_spy, ransomware_test_data, ransomware_options, build_ransomware
):
    file_not_exists = "/file/not/exist"
    mfe = MagicMock(
        side_effect=FileNotFoundError(f"[Errno 2] No such file or directory: '{file_not_exists}'")
    )
    mfs = MagicMock(return_value=[PurePosixPath(file_not_exists)])
    ransomware = build_ransomware(config=ransomware_options, file_encryptor=mfe, file_selector=mfs)

    ransomware.run(threading.Event())

    assert len(agent_event_queue_spy.events) == 1

    for event in agent_event_queue_spy.events:
        assert event.__class__ is FileEncryptionEvent
        assert not event.success
        assert event.target is None
        assert event.file_path == PurePosixPath(file_not_exists)
