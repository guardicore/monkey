import sys
from copy import deepcopy
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

MONKEY_BASE_PATH = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, MONKEY_BASE_PATH)

from monkeytoolbox import get_os  # noqa: E402
from monkeytypes import OperatingSystem  # noqa: E402

from common.agent_configuration import DEFAULT_AGENT_CONFIGURATION, AgentConfiguration  # noqa: E402
from infection_monkey.network import ITCPPortSelector, TCPPortSelector  # noqa: E402


@pytest.fixture(scope="session")
def data_for_tests_dir(pytestconfig):
    return Path(pytestconfig.rootdir) / "monkey" / "tests" / "data_for_tests"


@pytest.fixture(scope="session")
def stable_file(data_for_tests_dir) -> Path:
    return data_for_tests_dir / "stable_file.txt"


@pytest.fixture(scope="session")
def stable_file_sha256_hash() -> str:
    return "d9dcaadc91261692dafa86e7275b1bf39bb7e19d2efcfacd6fe2bfc9a1ae1062"


@pytest.fixture(scope="session")
def agent_plugin_repository_index_file(data_for_tests_dir) -> Path:
    return data_for_tests_dir / "agent_plugin" / "agent_plugin_repository_index.yml"


@pytest.fixture(scope="session")
def agent_plugin_repository_index_simple_file(data_for_tests_dir) -> Path:
    return data_for_tests_dir / "agent_plugin" / "agent_plugin_repository_index_simple.yml"


@pytest.fixture
def home_env_variable():
    if get_os() == OperatingSystem.WINDOWS:
        return "%USERPROFILE%"
    else:
        return "$HOME"


@pytest.fixture
def patched_home_env(monkeypatch, tmp_path, home_env_variable):
    monkeypatch.setenv(home_env_variable.strip("%$"), str(tmp_path))

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
def plugin_data_dir(data_for_tests_dir) -> Path:
    return data_for_tests_dir / "plugins"


@pytest.fixture
def default_agent_configuration() -> AgentConfiguration:
    return deepcopy(DEFAULT_AGENT_CONFIGURATION)


@pytest.fixture(scope="session")
def tcp_port_selector() -> ITCPPortSelector:
    return TCPPortSelector()
