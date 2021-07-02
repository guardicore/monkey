import os
import sys
from pathlib import Path

import pytest

MONKEY_BASE_PATH = str(Path(__file__).parent.parent)
sys.path.insert(0, MONKEY_BASE_PATH)


@pytest.fixture(scope="session")
def data_for_tests_dir(pytestconfig):
    return os.path.join(pytestconfig.rootdir, "monkey", "tests", "data_for_tests")
