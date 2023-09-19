import threading
from pathlib import Path
from unittest.mock import MagicMock

import agent_plugins.payloads.ransomware.src.ransomware_builder as ransomware_builder
import pytest
from agent_plugins.payloads.ransomware.src.ransomware_options import RansomwareOptions

from common import OperatingSystem
from common.event_queue import IAgentEventPublisher
from common.types import AgentID
from common.utils.environment import get_os

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
def ransomware_options_dict(ransomware_file_extension: str, target_dir: Path) -> dict:
    if get_os() == OperatingSystem.LINUX:
        return RansomwareOptions(
            file_extension=ransomware_file_extension,
            linux_target_dir=str(target_dir),
        )

    return RansomwareOptions(
        file_extension=ransomware_file_extension,
        windows_target_dir=str(target_dir),
    )


def test_uses_correct_extension(
    ransomware_options_dict: dict,
    target_file: Path,
    ransomware_file_extension: str,
):
    ransomware = ransomware_builder.build_ransomware(
        AGENT_ID, MagicMock(spec=IAgentEventPublisher), ransomware_options_dict
    )

    ransomware.run(threading.Event())

    # Verify that the file has been encrypted with the correct ending
    encrypted_file = target_file.with_suffix(target_file.suffix + ransomware_file_extension)
    assert encrypted_file.is_file()
