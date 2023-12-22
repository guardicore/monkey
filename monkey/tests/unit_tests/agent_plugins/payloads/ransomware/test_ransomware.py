import os
import threading
from pathlib import Path, PurePosixPath
from typing import Callable, Type, TypeAlias
from unittest.mock import MagicMock

import pytest
from agent_plugins.payloads.ransomware.src.consts import README_FILE_NAME, README_SRC
from agent_plugins.payloads.ransomware.src.internal_ransomware_options import (
    InternalRansomwareOptions,
)
from agent_plugins.payloads.ransomware.src.ransomware import Ransomware
from agent_plugins.payloads.ransomware.src.typedef import (
    FileEncryptorCallable,
    FileSelectorCallable,
    ReadmeDropperCallable,
    WallpaperChangerCallable,
)
from monkeyevents import AbstractAgentEvent, FileEncryptionEvent
from monkeytypes import AgentID, Event
from tests.unit_tests.agent_plugins.payloads.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    HELLO_TXT,
    TEST_KEYBOARD_TXT,
)
from tests.utils import is_user_admin

from common.event_queue import AgentEventSubscriber, IAgentEventPublisher

BuildRansomwareCallable: TypeAlias = Callable[
    [
        InternalRansomwareOptions,
        FileEncryptorCallable,
        FileSelectorCallable,
        ReadmeDropperCallable,
        WallpaperChangerCallable,
    ],
    Ransomware,
]


class AgentEventPublisherSpy(IAgentEventPublisher):
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
def agent_event_publisher_spy() -> IAgentEventPublisher:
    return AgentEventPublisherSpy()


@pytest.fixture
def ransomware(
    build_ransomware: BuildRansomwareCallable,
    internal_ransomware_options: InternalRansomwareOptions,
) -> Ransomware:
    return build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]


@pytest.fixture
def build_ransomware(
    mock_file_encryptor: FileEncryptorCallable,
    mock_file_selector: FileSelectorCallable,
    mock_leave_readme: ReadmeDropperCallable,
    mock_wallpaper_changer: WallpaperChangerCallable,
    agent_event_publisher_spy: IAgentEventPublisher,
) -> BuildRansomwareCallable:
    def inner(
        config: InternalRansomwareOptions,
        file_encryptor: FileEncryptorCallable = mock_file_encryptor,
        file_selector: FileSelectorCallable = mock_file_selector,
        leave_readme: ReadmeDropperCallable = mock_leave_readme,
        change_wallpaper: WallpaperChangerCallable = mock_wallpaper_changer,
    ) -> Ransomware:
        return Ransomware(
            config,
            file_encryptor,
            file_selector,
            leave_readme,
            change_wallpaper,
            agent_event_publisher_spy,
            AgentID("8f53f4fb-2d33-465a-aa9c-de704a7e42b3"),
        )

    return inner


@pytest.fixture
def internal_ransomware_options(
    ransomware_file_extension: str, ransomware_test_data: Path
) -> InternalRansomwareOptions:
    class InternalRansomwareOptionsStub(InternalRansomwareOptions):
        def __init__(
            self,
            leave_readme: bool,
            change_wallpaper: bool,
            file_extension: str,
            target_directory: Path,
        ):
            self.leave_readme = leave_readme
            self.change_wallpaper = change_wallpaper
            self.file_extension = file_extension
            self.target_directory = target_directory

    return InternalRansomwareOptionsStub(
        False, False, ransomware_file_extension, ransomware_test_data
    )


@pytest.fixture
def mock_file_encryptor() -> FileEncryptorCallable:
    return MagicMock()


@pytest.fixture
def mock_file_selector(ransomware_test_data) -> FileSelectorCallable:
    selected_files = iter(
        [
            ransomware_test_data / ALL_ZEROS_PDF,
            ransomware_test_data / TEST_KEYBOARD_TXT,
        ]
    )
    return MagicMock(return_value=selected_files)


@pytest.fixture
def mock_leave_readme() -> ReadmeDropperCallable:
    return MagicMock()


@pytest.fixture
def mock_wallpaper_changer() -> WallpaperChangerCallable:
    return MagicMock()


@pytest.fixture
def interrupt() -> Event:
    return threading.Event()


def test_files_selected_from_target_dir(
    ransomware: Ransomware,
    internal_ransomware_options: InternalRansomwareOptions,
    mock_file_selector: FileSelectorCallable,
):
    ransomware.run(threading.Event())
    mock_file_selector.assert_called_with(internal_ransomware_options.target_directory)


def test_all_selected_files_encrypted(
    ransomware_test_data: Path, ransomware: Ransomware, mock_file_encryptor: FileEncryptorCallable
):
    ransomware.run(threading.Event())

    assert mock_file_encryptor.call_count == 2
    mock_file_encryptor.assert_any_call(ransomware_test_data / ALL_ZEROS_PDF)
    mock_file_encryptor.assert_any_call(ransomware_test_data / TEST_KEYBOARD_TXT)


def test_interrupt_while_encrypting(
    ransomware_test_data: Path,
    interrupt: Event,
    internal_ransomware_options: InternalRansomwareOptions,
    build_ransomware: BuildRansomwareCallable,
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

    build_ransomware(internal_ransomware_options, mfe, mfs).run(interrupt)  # type: ignore [call-arg]  # noqa: E501

    assert mfe.call_count == 2
    mfe.assert_any_call(ransomware_test_data / ALL_ZEROS_PDF)
    mfe.assert_any_call(ransomware_test_data / HELLO_TXT)


def test_encryption_skipped_if_no_directory(
    build_ransomware: BuildRansomwareCallable,
    internal_ransomware_options: InternalRansomwareOptions,
    mock_file_encryptor: FileEncryptorCallable,
):
    internal_ransomware_options.target_directory = None

    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]
    ransomware.run(threading.Event())

    assert mock_file_encryptor.call_count == 0


def test_no_readme_after_interrupt(
    internal_ransomware_options: InternalRansomwareOptions,
    build_ransomware: BuildRansomwareCallable,
    interrupt: Event,
    mock_leave_readme: ReadmeDropperCallable,
):
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    interrupt.set()
    ransomware.run(interrupt)

    mock_leave_readme.assert_not_called()


def test_readme_false(
    build_ransomware: BuildRansomwareCallable,
    internal_ransomware_options: InternalRansomwareOptions,
    mock_leave_readme: ReadmeDropperCallable,
):
    internal_ransomware_options.leave_readme = False
    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    ransomware.run(threading.Event())
    mock_leave_readme.assert_not_called()


def test_readme_true(
    build_ransomware: BuildRansomwareCallable,
    internal_ransomware_options: InternalRansomwareOptions,
    mock_leave_readme: ReadmeDropperCallable,
    ransomware_test_data: Path,
):
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    ransomware.run(threading.Event())
    mock_leave_readme.assert_called_with(README_SRC, ransomware_test_data / README_FILE_NAME)


def test_no_readme_if_no_directory(
    build_ransomware: BuildRansomwareCallable,
    internal_ransomware_options: InternalRansomwareOptions,
    mock_leave_readme: ReadmeDropperCallable,
):
    internal_ransomware_options.target_directory = None
    internal_ransomware_options.leave_readme = True

    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    ransomware.run(threading.Event())
    mock_leave_readme.assert_not_called()


def test_leave_readme_exceptions_handled(
    build_ransomware: BuildRansomwareCallable,
    internal_ransomware_options: InternalRansomwareOptions,
):
    leave_readme = MagicMock(side_effect=Exception("Test exception when leaving README"))
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(config=internal_ransomware_options, leave_readme=leave_readme)  # type: ignore [call-arg]  # noqa: E501

    # Test will fail if exception is raised and not handled
    ransomware.run(threading.Event())


def test_no_wallpaper_change_after_interrupt(
    internal_ransomware_options: InternalRansomwareOptions,
    build_ransomware: BuildRansomwareCallable,
    interrupt: Event,
    mock_wallpaper_changer: WallpaperChangerCallable,
):
    internal_ransomware_options.change_wallpaper = True
    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    interrupt.set()
    ransomware.run(interrupt)

    mock_wallpaper_changer.assert_not_called()


def test_change_wallpaper_false(
    build_ransomware: BuildRansomwareCallable,
    internal_ransomware_options: InternalRansomwareOptions,
    mock_wallpaper_changer: WallpaperChangerCallable,
):
    internal_ransomware_options.change_wallpaper = False
    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    ransomware.run(threading.Event())
    mock_wallpaper_changer.assert_not_called()


def test_change_wallpaper_true(
    build_ransomware: BuildRansomwareCallable,
    internal_ransomware_options: InternalRansomwareOptions,
    mock_wallpaper_changer: WallpaperChangerCallable,
    ransomware_test_data: Path,
):
    internal_ransomware_options.change_wallpaper = True
    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    ransomware.run(threading.Event())
    mock_wallpaper_changer.call_count == 1


def test_change_wallpaper_exceptions_handled(
    build_ransomware: BuildRansomwareCallable,
    internal_ransomware_options: InternalRansomwareOptions,
):
    change_wallpaper = MagicMock(side_effect=Exception("Test exception when changing wallpaper"))
    internal_ransomware_options.change_wallpaper = True
    ransomware = build_ransomware(config=internal_ransomware_options, change_wallpaper=change_wallpaper)  # type: ignore [call-arg]  # noqa: E501

    # Test will fail if exception is raised and not handled
    ransomware.run(threading.Event())


def test_file_encryption_event_publishing(
    agent_event_publisher_spy: IAgentEventPublisher,
    ransomware_test_data: Path,
    internal_ransomware_options: InternalRansomwareOptions,
    build_ransomware: BuildRansomwareCallable,
):
    expected_selected_files = [
        ransomware_test_data / ALL_ZEROS_PDF,
        ransomware_test_data / HELLO_TXT,
        ransomware_test_data / TEST_KEYBOARD_TXT,
    ]
    mfs = MagicMock(return_value=expected_selected_files)

    build_ransomware(internal_ransomware_options, MagicMock(), mfs).run(threading.Event())  # type: ignore [call-arg]  # noqa: E501

    assert len(agent_event_publisher_spy.events) == 3

    for event in agent_event_publisher_spy.events:
        assert event.__class__ is FileEncryptionEvent
        assert event.success
        assert event.target is None

    actual_file_paths = [event.file_path for event in agent_event_publisher_spy.events]
    assert expected_selected_files == actual_file_paths


def test_file_encryption_event_publishing__failed(
    agent_event_publisher_spy: IAgentEventPublisher,
    ransomware_test_data: Path,
    internal_ransomware_options: InternalRansomwareOptions,
    build_ransomware: BuildRansomwareCallable,
):
    file_not_exists = "/file/not/exist"
    mfe = MagicMock(
        side_effect=FileNotFoundError(f"[Errno 2] No such file or directory: '{file_not_exists}'")
    )
    mfs = MagicMock(return_value=[PurePosixPath(file_not_exists)])
    ransomware = build_ransomware(  # type: ignore [call-arg]
        config=internal_ransomware_options, file_encryptor=mfe, file_selector=mfs
    )

    ransomware.run(threading.Event())

    assert len(agent_event_publisher_spy.events) == 1

    for event in agent_event_publisher_spy.events:
        assert event.__class__ is FileEncryptionEvent
        assert not event.success
        assert event.target is None
        assert event.file_path == PurePosixPath(file_not_exists)


def test_no_action_if_directory_doesnt_exist(
    internal_ransomware_options: InternalRansomwareOptions,
    build_ransomware: BuildRansomwareCallable,
    mock_file_selector: FileSelectorCallable,
    mock_leave_readme: ReadmeDropperCallable,
):
    internal_ransomware_options.target_directory = Path("/noexist")
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    ransomware.run(threading.Event())

    mock_file_selector.assert_not_called()
    mock_leave_readme.assert_not_called()


def test_no_action_if_directory_is_file(
    tmp_path: Path,
    internal_ransomware_options: InternalRansomwareOptions,
    build_ransomware: BuildRansomwareCallable,
    mock_file_selector: FileSelectorCallable,
    mock_leave_readme: ReadmeDropperCallable,
):
    target_file = tmp_path / "target_file.txt"
    target_file.touch()
    assert target_file.exists()
    assert target_file.is_file()

    internal_ransomware_options.target_directory = target_file
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    ransomware.run(threading.Event())

    mock_file_selector.assert_not_called()
    mock_leave_readme.assert_not_called()


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
def test_no_action_if_directory_is_symlink(
    tmp_path: Path,
    internal_ransomware_options: InternalRansomwareOptions,
    build_ransomware: BuildRansomwareCallable,
    mock_file_selector: FileSelectorCallable,
    mock_leave_readme: ReadmeDropperCallable,
):
    link_target = tmp_path / "link_target"
    link_target.mkdir()
    assert link_target.exists()
    assert link_target.is_dir()

    link = tmp_path / "link"
    link.symlink_to(link_target, target_is_directory=True)

    internal_ransomware_options.target_directory = link
    internal_ransomware_options.leave_readme = True
    ransomware = build_ransomware(internal_ransomware_options)  # type: ignore [call-arg]

    ransomware.run(threading.Event())

    mock_file_selector.assert_not_called()
    mock_leave_readme.assert_not_called()
