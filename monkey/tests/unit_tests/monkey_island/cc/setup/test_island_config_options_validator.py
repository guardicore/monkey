import os
import subprocess
from collections.abc import Callable

import pytest

from common.utils.exceptions import InsecurePermissionsError
from monkey_island.cc.setup.island_config_options import IslandConfigOptions
from monkey_island.cc.setup.island_config_options_validator import raise_on_invalid_options

LINUX_READ_ONLY_BY_USER = 0o400
LINUX_RWX_BY_ALL = 0o777


def certificate_test_island_config_options(crt_file, key_file):
    return IslandConfigOptions(
        {
            "ssl_certificate": {
                "ssl_certificate_file": crt_file,
                "ssl_certificate_key_file": key_file,
            }
        }
    )


@pytest.fixture
def linux_island_config_options(create_read_only_linux_file: Callable):
    crt_file = create_read_only_linux_file("test.crt")
    key_file = create_read_only_linux_file("test.key")

    return certificate_test_island_config_options(crt_file, key_file)


@pytest.fixture
def create_read_only_linux_file(tmpdir: str, create_empty_tmp_file: Callable) -> Callable:
    def inner(file_name: str) -> str:
        full_file_path = create_empty_tmp_file(file_name)
        os.chmod(full_file_path, LINUX_READ_ONLY_BY_USER)

        return full_file_path

    return inner


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_linux_valid_crt_and_key_paths(linux_island_config_options):
    try:
        raise_on_invalid_options(linux_island_config_options)
    except Exception as ex:
        print(ex)
        assert False


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_linux_crt_path_does_not_exist(linux_island_config_options):
    os.remove(linux_island_config_options.crt_path)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(linux_island_config_options)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_linux_crt_path_insecure_permissions(linux_island_config_options):
    os.chmod(linux_island_config_options.crt_path, LINUX_RWX_BY_ALL)

    with pytest.raises(InsecurePermissionsError):
        raise_on_invalid_options(linux_island_config_options)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_linux_key_path_does_not_exist(linux_island_config_options):
    os.remove(linux_island_config_options.key_path)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(linux_island_config_options)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_linux_key_path_insecure_permissions(linux_island_config_options):
    os.chmod(linux_island_config_options.key_path, LINUX_RWX_BY_ALL)

    with pytest.raises(InsecurePermissionsError):
        raise_on_invalid_options(linux_island_config_options)


@pytest.fixture
def windows_island_config_options(tmpdir: str, create_read_only_windows_file: Callable):
    crt_file = create_read_only_windows_file("test.crt")
    key_file = create_read_only_windows_file("test.key")

    return certificate_test_island_config_options(crt_file, key_file)


@pytest.fixture
def create_read_only_windows_file(tmpdir: str, create_empty_tmp_file: Callable) -> Callable:
    def inner(file_name: str) -> str:
        full_file_path = create_empty_tmp_file(file_name)
        cmd_to_change_permissions = get_windows_cmd_to_change_permissions(full_file_path, "R")
        subprocess.run(cmd_to_change_permissions, shell=True)  # noqa DUO116

        return full_file_path

    return inner


def get_windows_cmd_to_change_permissions(file_name, permissions):
    """
    :param file_name: name of file
    :param permissions: can be: N (None), R (Read), W (Write), C (Change (write)), F (Full control)
    """
    return f"echo y| cacls {file_name} /p %USERNAME%:{permissions}"


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_windows_valid_crt_and_key_paths(windows_island_config_options):
    try:
        raise_on_invalid_options(windows_island_config_options)
    except Exception as ex:
        print(ex)
        assert False


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_windows_crt_path_does_not_exist(windows_island_config_options):
    os.remove(windows_island_config_options.crt_path)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(windows_island_config_options)


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_windows_crt_path_insecure_permissions(windows_island_config_options):
    cmd_to_change_permissions = get_windows_cmd_to_change_permissions(
        windows_island_config_options.crt_path, "W"
    )
    subprocess.run(cmd_to_change_permissions, shell=True)  # noqa DUO116

    with pytest.raises(InsecurePermissionsError):
        raise_on_invalid_options(windows_island_config_options)


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_windows_key_path_does_not_exist(windows_island_config_options):
    os.remove(windows_island_config_options.key_path)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(windows_island_config_options)


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_windows_key_path_insecure_permissions(windows_island_config_options):
    cmd_to_change_permissions = get_windows_cmd_to_change_permissions(
        windows_island_config_options.key_path, "W"
    )
    subprocess.run(cmd_to_change_permissions, shell=True)  # noqa DUO116

    with pytest.raises(InsecurePermissionsError):
        raise_on_invalid_options(windows_island_config_options)
