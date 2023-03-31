from typing import Collection, Dict, Mapping, Set

import pytest

from envs.monkey_zoo.blackbox.gcp_test_machine_list import GCP_SINGLE_TEST_LIST


def pytest_addoption(parser):
    parser.addoption(
        "--island",
        action="store",
        default="",
        help="Specify the Monkey Island address (host+port).",
    )
    parser.addoption(
        "--no-gcp",
        action="store_true",
        default=False,
        help="Use for no interaction with the cloud.",
    )


@pytest.fixture(scope="session")
def island(request):
    return request.config.getoption("--island")


@pytest.fixture(scope="session")
def no_gcp(request):
    return request.config.getoption("--no-gcp")


@pytest.fixture(scope="session")
def gcp_machines_to_start(request: pytest.FixtureRequest) -> Mapping[str, Collection[str]]:
    machines_to_start: Dict[str, Set[str]] = {}

    enabled_tests = (test.originalname for test in request.node.items)
    machines_for_enabled_tests = (GCP_SINGLE_TEST_LIST.get(test, {}) for test in enabled_tests)

    for machine_dict in machines_for_enabled_tests:
        for zone, machines in machine_dict.items():
            machines_to_start.setdefault(zone, set()).update(machines)

    return machines_to_start
