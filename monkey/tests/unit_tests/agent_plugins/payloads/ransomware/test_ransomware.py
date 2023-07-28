import os
import threading
from pathlib import Path, PurePosixPath
from typing import Type
from unittest.mock import MagicMock

import pytest
from agent_plugins.payloads.ransomware.src.consts import README_FILE_NAME, README_SRC
from agent_plugins.payloads.ransomware.src.internal_ransomware_options import (
    InternalRansomwareOptions,
)
from agent_plugins.payloads.ransomware.src.ransomware import Ransomware
from tests.unit_tests.agent_plugins.payloads.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    HELLO_TXT,
    TEST_KEYBOARD_TXT,
)
from tests.utils import is_user_admin

from common.agent_events import AbstractAgentEvent, FileEncryptionEvent
from common.event_queue import AgentEventSubscriber, IAgentEventQueue
from common.types import AgentID


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
def ransomware(build_ransomware, internal_ransomware_options):
    return build_ransomware(internal_ransomware_options)


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
            AgentID("8f53f4fb-2d33-465a-aa9c-de704a7e42b3"),
        )

    return inner


@pytest.fixture
def internal_ransomware_options(ransomware_file_extension, ransomware_test_data):
    class InternalRansomwareOptionsStub(InternalRansomwareOptions):
        def __init__(self, leave_readme, file_extension, target_directory):
            self.leave_readme = leave_readme
            self.file_extension = file_extension
            self.target_directory = target_directory

    return InternalRansomwareOptionsStub(False, ransomware_file_extension, ransomware_test_data)


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
    internal_ransomware_options,
    mock_file_selector,
):
    ransomware.run(threading.Event())
    mock_file_selector.assert_called_with(internal_ransomware_options.target_directory)


def test_all_selected_files_encrypted(ransomware_test_data, ransomware, mock_file_encryptor):
    ransomware.run(threading.Event())

    assert mock_file_encryptor.call_count == 2
    mock_file_encryptor.assert_any_call(ransomware_test_data / ALL_ZEROS_PDF)
    mock_file_encryptor.assert_any_call(ransomware_test_data / TEST_KEYBOARD_TXT)


def test_interrupt_while_encrypting(
    ransomware_test_data, interrupt, internal_ransomware_options, build_ransomware
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

    build_ransomware(internal_ransomware_options, mfe, mfs).run(interrupt)

    assert mfe.call_count == 2
    mfe.assert_any_call(ransomware_test_data / ALL_ZEROS_PDF)
    mfe.assert_any_call(ransomware_test_data / HELLO_TXT)


def test_no_readme_after_interrupt(
    internal_ransomware_options, build_ransomware, interrupt, mock_leave_readme
):
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)

    interrupt.set()
    ransomware.run(interrupt)

    mock_leave_readme.assert_not_called()


def test_encryption_skipped_if_no_directory(
    build_ransomware, internal_ransomware_options, mock_file_encryptor
):
    internal_ransomware_options.target_directory = None

    ransomware = build_ransomware(internal_ransomware_options)
    ransomware.run(threading.Event())

    assert mock_file_encryptor.call_count == 0


def test_readme_false(build_ransomware, internal_ransomware_options, mock_leave_readme):
    internal_ransomware_options.leave_readme = False
    ransomware = build_ransomware(internal_ransomware_options)

    ransomware.run(threading.Event())
    mock_leave_readme.assert_not_called()


def test_readme_true(
    build_ransomware, internal_ransomware_options, mock_leave_readme, ransomware_test_data
):
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)

    ransomware.run(threading.Event())
    mock_leave_readme.assert_called_with(README_SRC, ransomware_test_data / README_FILE_NAME)


def test_no_readme_if_no_directory(
    build_ransomware, internal_ransomware_options, mock_leave_readme
):
    internal_ransomware_options.target_directory = None
    internal_ransomware_options.leave_readme = True

    ransomware = build_ransomware(internal_ransomware_options)

    ransomware.run(threading.Event())
    mock_leave_readme.assert_not_called()


def test_leave_readme_exceptions_handled(build_ransomware, internal_ransomware_options):
    leave_readme = MagicMock(side_effect=Exception("Test exception when leaving README"))
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(config=internal_ransomware_options, leave_readme=leave_readme)

    # Test will fail if exception is raised and not handled
    ransomware.run(threading.Event())


def test_file_encryption_event_publishing(
    agent_event_queue_spy, ransomware_test_data, internal_ransomware_options, build_ransomware
):
    expected_selected_files = [
        ransomware_test_data / ALL_ZEROS_PDF,
        ransomware_test_data / HELLO_TXT,
        ransomware_test_data / TEST_KEYBOARD_TXT,
    ]
    mfs = MagicMock(return_value=expected_selected_files)

    build_ransomware(internal_ransomware_options, MagicMock(), mfs).run(threading.Event())

    assert len(agent_event_queue_spy.events) == 3

    for event in agent_event_queue_spy.events:
        assert event.__class__ is FileEncryptionEvent
        assert event.success
        assert event.target is None

    actual_file_paths = [event.file_path for event in agent_event_queue_spy.events]
    assert expected_selected_files == actual_file_paths


def test_file_encryption_event_publishing__failed(
    agent_event_queue_spy, ransomware_test_data, internal_ransomware_options, build_ransomware
):
    file_not_exists = "/file/not/exist"
    mfe = MagicMock(
        side_effect=FileNotFoundError(f"[Errno 2] No such file or directory: '{file_not_exists}'")
    )
    mfs = MagicMock(return_value=[PurePosixPath(file_not_exists)])
    ransomware = build_ransomware(
        config=internal_ransomware_options, file_encryptor=mfe, file_selector=mfs
    )

    ransomware.run(threading.Event())

    assert len(agent_event_queue_spy.events) == 1

    for event in agent_event_queue_spy.events:
        assert event.__class__ is FileEncryptionEvent
        assert not event.success
        assert event.target is None
        assert event.file_path == PurePosixPath(file_not_exists)


def test_no_action_if_directory_doesnt_exist(
    internal_ransomware_options, build_ransomware, mock_file_selector, mock_leave_readme
):
    internal_ransomware_options.target_directory = Path("/noexist")
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)

    ransomware.run(threading.Event())

    mock_file_selector.assert_not_called()
    mock_leave_readme.assert_not_called()


def test_no_action_if_directory_is_file(
    tmp_path, internal_ransomware_options, build_ransomware, mock_file_selector, mock_leave_readme
):
    target_file = tmp_path / "target_file.txt"
    target_file.touch()
    assert target_file.exists()
    assert target_file.is_file()

    internal_ransomware_options.target_directory = target_file
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)

    ransomware.run(threading.Event())

    mock_file_selector.assert_not_called()
    mock_leave_readme.assert_not_called()


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
def test_no_action_if_directory_is_symlink(
    tmp_path, internal_ransomware_options, build_ransomware, mock_file_selector, mock_leave_readme
):
    link_target = tmp_path / "link_target"
    link_target.mkdir()
    assert link_target.exists()
    assert link_target.is_dir()

    link = tmp_path / "link"
    link.symlink_to(link_target, target_is_directory=True)

    internal_ransomware_options.target_directory = link
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)

    ransomware.run(threading.Event())

    mock_file_selector.assert_not_called()
    mock_leave_readme.assert_not_called()
