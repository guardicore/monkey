import pytest

from envs.monkey_zoo.blackbox.gcp_test_machine_list import (
    GCP_SINGLE_TEST_LIST,
    GCP_TEST_MACHINE_LIST,
)


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
    parser.addoption(
        "--skip-powershell-reuse",
        action="store_true",
        default=False,
        help="Use to run PowerShell credentials reuse test.",
    )


@pytest.fixture(scope="session")
def island(request):
    return request.config.getoption("--island")


@pytest.fixture(scope="session")
def no_gcp(request):
    return request.config.getoption("--no-gcp")


@pytest.fixture(scope="session")
def list_machines(request):
    enabled_tests = [test.name for test in request.node.items]

    if len(enabled_tests) == len(GCP_SINGLE_TEST_LIST.keys()):
        return GCP_TEST_MACHINE_LIST

    try:
        list_machines_to_start = [GCP_SINGLE_TEST_LIST[test] for test in enabled_tests]

        if len(list_machines_to_start) == 1:
            return list_machines_to_start[0]

        single_machine_list = {}

        for machine_dict in list_machines_to_start:
            for zone, machines in machine_dict.items():
                for machine in machines:
                    if machine not in single_machine_list[zone]:
                        single_machine_list[zone].append(machine)

    except KeyError:
        return GCP_TEST_MACHINE_LIST

    return single_machine_list


def pytest_runtest_setup(item):
    if "skip_powershell_reuse" in item.keywords and item.config.getoption(
        "--skip-powershell-reuse"
    ):
        pytest.skip(
            "Skipping powershell credentials reuse test because "
            "--skip-powershell-cached flag isn't specified."
        )
