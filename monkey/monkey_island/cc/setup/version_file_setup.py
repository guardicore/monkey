from pathlib import Path

from packaging import version

from common.version import get_version

_version_filename = "VERSION"


def get_version_from_dir(dir_path: str) -> str:
    version_file_path = Path(dir_path, _version_filename)
    return version_file_path.read_text()


def write_version(dir_path: str):
    version_file_path = Path(dir_path, _version_filename)
    version_file_path.write_text(get_version())


def is_version_greater(version1: str, version2: str) -> bool:
    return version.parse(version1) > version.parse(version2)
