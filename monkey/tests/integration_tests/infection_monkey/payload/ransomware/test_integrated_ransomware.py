import threading
from copy import deepcopy
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import infection_monkey.payload.ransomware.ransomware_builder as ransomware_builder
from common.agent_configuration.default_agent_configuration import RANSOMWARE_OPTIONS
from common.event_queue import IAgentEventQueue
from common.types import AgentID

AGENT_ID = AgentID("0442ca83-10ce-495f-9c1c-92b4e1f5c39c")


@pytest.fixture
def target_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def target_file(target_dir: Path) -> Path:
    file = target_dir / "file.txt"
    file.write_text("Do your worst!")

    return file


@pytest.fixture
def ransomware_options_dict(target_dir: Path) -> dict:
    options = deepcopy(RANSOMWARE_OPTIONS)

    ransomware_directories = options["encryption"]["directories"]
    ransomware_directories["linux_target_dir"] = target_dir
    ransomware_directories["windows_target_dir"] = target_dir

    # Leaving a readme is slow and not relevant for these tests
    options["other_behaviors"]["readme"] = False

    return options


def test_uses_correct_extension(
    ransomware_options_dict: dict,
    target_file: Path,
    ransomware_file_extension: str,
):
    ransomware_options_dict["encryption"]["file_extension"] = ransomware_file_extension
    ransomware = ransomware_builder.build_ransomware(
        ransomware_options_dict, MagicMock(spec=IAgentEventQueue), AGENT_ID
    )

    ransomware.run(threading.Event())

    # Verify that the file has been encrypted with the correct ending
    encrypted_file = target_file.with_suffix(target_file.suffix + ransomware_file_extension)
    assert encrypted_file.is_file()


def test_uses_aes256(
    ransomware_options_dict: dict,
    target_file: Path,
):
    ransomware_options_dict["encryption"]["algorithm"] = "aes256"
    ransomware_options_dict["encryption"]["file_extension"] = ""
    ransomware = ransomware_builder.build_ransomware(
        ransomware_options_dict, MagicMock(spec=IAgentEventQueue), AGENT_ID
    )

    original_size = target_file.stat().st_size
    ransomware.run(threading.Event())

    assert target_file.stat().st_size > original_size
    assert b"pyAesCrypt" in target_file.read_bytes()


def test_uses_bit_flip(
    ransomware_options_dict: dict,
    target_file: Path,
):
    ransomware_options_dict["encryption"]["algorithm"] = "bit_flip"
    ransomware_options_dict["encryption"]["file_extension"] = ""
    ransomware = ransomware_builder.build_ransomware(
        ransomware_options_dict, MagicMock(spec=IAgentEventQueue), AGENT_ID
    )

    original_size = target_file.stat().st_size
    ransomware.run(threading.Event())

    assert target_file.stat().st_size == original_size
    assert target_file.read_bytes() == b"\xbb\x90\xdf\x86\x90\x8a\x8d\xdf\x88\x90\x8d\x8c\x8b\xde"
