import logging
import string
from pathlib import PurePath, PurePosixPath, PureWindowsPath

from agentpluginapi import TargetHost
from monkeytoolbox import insecure_generate_random_string
from monkeytypes import OperatingSystem

logger = logging.getLogger(__name__)

RAND_SUFFIX_LEN = 8

# Where to upload agent binaries on victims
AGENT_BINARY_PATH_LINUX = PurePosixPath("/tmp/monkey")
AGENT_BINARY_PATH_WIN64 = PureWindowsPath(r"C:\Windows\temp\monkey64.exe")

DROPPER_SCRIPT_PATH_LINUX = PurePosixPath("/tmp/monkey-dropper.sh")


def get_agent_dst_path(host: TargetHost) -> PurePath:
    return _add_random_suffix(_get_agent_path(host))


def _get_agent_path(host: TargetHost) -> PurePath:
    if host.operating_system == OperatingSystem.WINDOWS:
        return PureWindowsPath(AGENT_BINARY_PATH_WIN64)
    return PurePosixPath(AGENT_BINARY_PATH_LINUX)


#  Turns C:\\monkey.exe into C:\\monkey-<random_string>.exe
#  Useful to avoid duplicate file paths
def _add_random_suffix(path: PurePath) -> PurePath:
    stem = path.name.split(".")[0]
    stem = f"{stem}-{get_random_file_suffix()}"
    rand_filename = "".join([stem, *path.suffixes])
    return path.with_name(rand_filename)


def get_random_file_suffix() -> str:
    character_set = string.ascii_letters + string.digits + "_" + "-"
    # Avoid the risk of blocking by using insecure_generate_random_string()
    return insecure_generate_random_string(n=RAND_SUFFIX_LEN, character_set=character_set)


def get_dropper_script_dst_path(host: TargetHost) -> PurePath:
    return _add_random_suffix(_get_dropper_script_path(host))


def _get_dropper_script_path(host: TargetHost) -> PurePath:
    if host.operating_system == OperatingSystem.WINDOWS:
        raise NotImplementedError("This function is not implemented for Windows")

    return PurePosixPath(DROPPER_SCRIPT_PATH_LINUX)
