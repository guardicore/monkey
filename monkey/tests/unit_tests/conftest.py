import json
import sys
from pathlib import Path
from typing import Callable, Dict

import pytest
from _pytest.monkeypatch import MonkeyPatch
from tests.data_for_tests.monkey_configs.default_config import DEFAULT_CONFIG

from common.configuration import AgentConfiguration

MONKEY_BASE_PATH = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, MONKEY_BASE_PATH)

from common.configuration import AgentConfiguration, build_default_agent_configuration  # noqa: E402


@pytest.fixture(scope="session")
def data_for_tests_dir(pytestconfig):
    return Path(pytestconfig.rootdir) / "monkey" / "tests" / "data_for_tests"


@pytest.fixture(scope="session")
def stable_file(data_for_tests_dir) -> Path:
    return data_for_tests_dir / "stable_file.txt"


@pytest.fixture(scope="session")
def stable_file_sha256_hash() -> str:
    return "d9dcaadc91261692dafa86e7275b1bf39bb7e19d2efcfacd6fe2bfc9a1ae1062"


@pytest.fixture
def patched_home_env(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))

    return tmp_path


# The monkeypatch fixture is function scoped, so it cannot be used by session-scoped fixtures. This
# monkeypatch_session fixture can be session-scoped. For more information, see
# https://github.com/pytest-dev/pytest/issues/363#issuecomment-406536200
@pytest.fixture(scope="session")
def monkeypatch_session():
    monkeypatch_ = MonkeyPatch()
    yield monkeypatch_
    monkeypatch_.undo()


@pytest.fixture
def monkey_configs_dir(data_for_tests_dir) -> Path:
    return data_for_tests_dir / "monkey_configs"


@pytest.fixture
def load_monkey_config(data_for_tests_dir) -> Callable[[str], Dict]:
    def inner(filename: str) -> Dict:
        config_path = data_for_tests_dir / "monkey_configs" / filename
        return json.loads(open(config_path, "r").read())

    return inner


@pytest.fixture
def default_agent_configuration() -> AgentConfiguration:
    return build_default_agent_configuration()
