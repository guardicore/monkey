import pytest


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
        "--quick-performance-tests",
        action="store_true",
        default=False,
        help="If enabled performance tests won't reset island and won't send telemetries, "
        "instead will just test performance of already present island state.",
    )
    parser.addoption(
        "--run-performance-tests",
        action="store_true",
        default=False,
        help="If enabled performance tests will be run.",
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
def quick_performance_tests(request):
    return request.config.getoption("--quick-performance-tests")


def pytest_runtest_setup(item):
    if "run_performance_tests" in item.keywords and not item.config.getoption(
        "--run-performance-tests"
    ):
        pytest.skip(
            "Skipping performance test because " "--run-performance-tests flag isn't specified."
        )

    if "skip_powershell_reuse" in item.keywords and item.config.getoption(
        "--skip-powershell-reuse"
    ):
        pytest.skip(
            "Skipping powershell credentials reuse test because "
            "--skip-powershell-cached flag isn't specified."
        )
