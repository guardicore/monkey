import os
from collections.abc import Callable

import pytest


@pytest.fixture(scope="module")
def server_configs_dir(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "server_configs")


@pytest.fixture
def create_empty_tmp_file(tmpdir: str) -> Callable:
    def inner(file_name: str):
        new_file = os.path.join(tmpdir, file_name)
        with open(new_file, "w"):
            pass

        return new_file

    return inner
