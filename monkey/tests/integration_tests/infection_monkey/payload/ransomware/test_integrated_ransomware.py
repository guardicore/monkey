import threading
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import infection_monkey.payload.ransomware.ransomware_builder as ransomware_builder
from common.agent_configuration.default_agent_configuration import RANSOMWARE_OPTIONS
from common.event_queue import IAgentEventQueue
from common.types import AgentID

AGENT_ID = AgentID("0442ca83-10ce-495f-9c1c-92b4e1f5c39c")


@dataclass
class TargetFile:
    file: Path
    contents: bytes
    inverted_contents: bytes


@pytest.fixture
def f1(target_dir: Path) -> TargetFile:
    tf = TargetFile(
        target_dir / "file.txt",
        b"Do your worst!",
        b"\xbb\x90\xdf\x86\x90\x8a\x8d\xdf\x88\x90\x8d\x8c\x8b\xde",
    )
    tf.file.write_bytes(tf.contents)

    return tf


@pytest.fixture
def f2(target_dir: Path) -> TargetFile:
    subdir = target_dir / "subdir"
    subdir.mkdir()

    tf = TargetFile(
        subdir / "file.txt",
        b"No loitering.",
        b"\xB1\x90\xDF\x93\x90\x96\x8B\x9A\x8D\x96\x91\x98\xD1",
    )
    tf.file.write_bytes(tf.contents)

    return tf


@pytest.fixture
def target_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def ransomware_options_dict(target_dir: Path) -> dict:
    options = deepcopy(RANSOMWARE_OPTIONS)

    options["encryption"]["recursive"] = False
    ransomware_directories = options["encryption"]["directories"]
    ransomware_directories["linux_target_dir"] = target_dir
    ransomware_directories["windows_target_dir"] = target_dir

    # Leaving a readme is slow and not relevant for these tests
    options["other_behaviors"]["readme"] = False

    return options


def test_uses_correct_extension(
    ransomware_options_dict: dict,
    f1: TargetFile,
    ransomware_file_extension: str,
):
    ransomware_options_dict["encryption"]["file_extension"] = ransomware_file_extension
    ransomware = ransomware_builder.build_ransomware(
        ransomware_options_dict, MagicMock(spec=IAgentEventQueue), AGENT_ID
    )

    ransomware.run(threading.Event())

    # Verify that the file has been encrypted with the correct ending
    encrypted_file = f1.file.with_suffix(f1.file.suffix + ransomware_file_extension)
    assert encrypted_file.is_file()


def test_uses_aes256(
    ransomware_options_dict: dict,
    f1: TargetFile,
):
    ransomware_options_dict["encryption"]["algorithm"] = "aes256"
    ransomware_options_dict["encryption"]["file_extension"] = ""
    ransomware = ransomware_builder.build_ransomware(
        ransomware_options_dict, MagicMock(spec=IAgentEventQueue), AGENT_ID
    )

    original_size = f1.file.stat().st_size
    ransomware.run(threading.Event())

    assert f1.file.stat().st_size > original_size
    assert b"pyAesCrypt" in f1.file.read_bytes()


def test_uses_bit_flip__not_recursive(
    ransomware_options_dict: dict,
    f1: TargetFile,
    f2: TargetFile,
):
    ransomware_options_dict["encryption"]["algorithm"] = "bit_flip"
    ransomware_options_dict["encryption"]["file_extension"] = ""
    ransomware_options_dict["encryption"]["recursive"] = False
    ransomware = ransomware_builder.build_ransomware(
        ransomware_options_dict, MagicMock(spec=IAgentEventQueue), AGENT_ID
    )

    original_size = f1.file.stat().st_size
    ransomware.run(threading.Event())

    assert f1.file.stat().st_size == original_size
    assert f1.file.read_bytes() == f1.inverted_contents
    assert f2.file.read_bytes() == f2.contents


def test_uses_bit_flip__recursive(
    ransomware_options_dict: dict,
    f1: TargetFile,
    f2: TargetFile,
):
    ransomware_options_dict["encryption"]["algorithm"] = "bit_flip"
    ransomware_options_dict["encryption"]["file_extension"] = ""
    ransomware_options_dict["encryption"]["recursive"] = True
    ransomware = ransomware_builder.build_ransomware(
        ransomware_options_dict, MagicMock(spec=IAgentEventQueue), AGENT_ID
    )

    original_size = f1.file.stat().st_size
    ransomware.run(threading.Event())

    assert f1.file.stat().st_size == original_size
    assert f1.file.read_bytes() == f1.inverted_contents
    assert f2.file.read_bytes() == f2.inverted_contents
