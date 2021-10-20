from pathlib import Path

from common.version import get_version

_version_filename = "VERSION"


def get_version_from_dir(dir_path: Path) -> str:
    version_file_path = dir_path / _version_filename
    return version_file_path.read_text()


def write_version(dir_path: Path):
    version_file_path = dir_path / _version_filename
    version_file_path.write_text(get_version())
