import os

import pytest

from common.utils.exceptions import InsecurePermissionsError
from monkey_island.cc.setup.island_config_options import IslandConfigOptions
from monkey_island.cc.setup.island_config_options_validator import raise_on_invalid_options


@pytest.fixture
def island_config_options(tmpdir, create_empty_file):
    crt_file = os.path.join(tmpdir, "test.crt")
    create_empty_file(crt_file)
    os.chmod(crt_file, 0o400)

    key_file = os.path.join(tmpdir, "test.key")
    create_empty_file(key_file)
    os.chmod(key_file, 0o400)
    return IslandConfigOptions(
        {
            "ssl_certificate": {
                "ssl_certificate_file": crt_file,
                "ssl_certificate_key_file": key_file,
            }
        }
    )


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_valid_crt_and_key_paths(island_config_options):
    try:
        raise_on_invalid_options(island_config_options)
    except Exception as ex:
        print(ex)
        assert False


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_crt_path_does_not_exist(island_config_options):
    os.remove(island_config_options.crt_path)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(island_config_options)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_crt_path_insecure_permissions(island_config_options):
    os.chmod(island_config_options.crt_path, 0o777)

    with pytest.raises(InsecurePermissionsError):
        raise_on_invalid_options(island_config_options)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_key_path_does_not_exist(island_config_options):
    os.remove(island_config_options.key_path)

    with pytest.raises(FileNotFoundError):
        raise_on_invalid_options(island_config_options)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_key_path_insecure_permissions(island_config_options):
    os.chmod(island_config_options.key_path, 0o777)

    with pytest.raises(InsecurePermissionsError):
        raise_on_invalid_options(island_config_options)
