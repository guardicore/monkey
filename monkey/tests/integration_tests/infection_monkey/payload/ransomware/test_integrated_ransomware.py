import threading
from unittest.mock import MagicMock

import pytest

import infection_monkey.payload.ransomware.ransomware_builder as ransomware_builder
from common.agent_configuration.default_agent_configuration import RANSOMWARE_OPTIONS
from common.event_queue import IAgentEventQueue


@pytest.fixture
def ransomware_options_dict(ransomware_file_extension):
    options = RANSOMWARE_OPTIONS
    options["encryption"]["file_extension"] = ransomware_file_extension
    return options


def test_uses_correct_extension(ransomware_options_dict, tmp_path, ransomware_file_extension):
    target_dir = tmp_path

    # Leaving a readme is slow and not relevant for this test
    ransomware_options_dict["other_behaviors"]["readme"] = False
    ransomware_directories = ransomware_options_dict["encryption"]["directories"]
    ransomware_directories["linux_target_dir"] = target_dir
    ransomware_directories["windows_target_dir"] = target_dir
    ransomware = ransomware_builder.build_ransomware(
        ransomware_options_dict, MagicMock(spec=IAgentEventQueue)
    )

    file = target_dir / "file.txt"
    file.write_text("Do your worst!")

    ransomware.run(threading.Event())

    # Verify that the file has been encrypted with the correct ending
    encrypted_file = file.with_suffix(file.suffix + ransomware_file_extension)
    assert encrypted_file.is_file()
