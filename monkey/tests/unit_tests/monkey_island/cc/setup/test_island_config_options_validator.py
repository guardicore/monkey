import os
from collections.abc import Callable

import pytest

from monkey_island.cc.setup.island_config_options import IslandConfigOptions
from monkey_island.cc.setup.island_config_options_validator import raise_on_invalid_options


def certificate_test_island_config_options(crt_file, key_file):
    return IslandConfigOptions(
        ssl_certificate={
            "ssl_certificate_file": crt_file,
            "ssl_certificate_key_file": key_file,
        }
    )


@pytest.fixture
def linux_island_config_options(create_empty_tmp_file: Callable):
    crt_file = create_empty_tmp_file("test.crt")
    key_file = create_empty_tmp_file("test.key")

    return certificate_test_island_config_options(crt_file, key_file)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_linux_valid_crt_and_key_paths(linux_island_config_options):
    try:
        raise_on_invalid_options(linux_island_config_options)
    except Exception as ex:
        print(ex)
        assert False


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_linux_crt_path_does_not_exist(linux_island_config_options):
    os.remove(linux_island_config_options.ssl_certificate.ssl_certificate_file)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(linux_island_config_options)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_linux_key_path_does_not_exist(linux_island_config_options):
    os.remove(linux_island_config_options.ssl_certificate.ssl_certificate_key_file)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(linux_island_config_options)


@pytest.fixture
def windows_island_config_options(tmpdir: str, create_empty_tmp_file: Callable):
    crt_file = create_empty_tmp_file("test.crt")
    key_file = create_empty_tmp_file("test.key")

    return certificate_test_island_config_options(crt_file, key_file)


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_windows_valid_crt_and_key_paths(windows_island_config_options):
    try:
        raise_on_invalid_options(windows_island_config_options)
    except Exception as ex:
        print(ex)
        assert False


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_windows_crt_path_does_not_exist(windows_island_config_options):
    os.remove(windows_island_config_options.ssl_certificate.ssl_certificate_file)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(windows_island_config_options)


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_windows_key_path_does_not_exist(windows_island_config_options):
    os.remove(windows_island_config_options.ssl_certificate.ssl_certificate_key_file)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(windows_island_config_options)
