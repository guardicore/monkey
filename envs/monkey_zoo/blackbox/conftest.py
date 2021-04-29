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
        "--no-performance-tests",
        action="store_true",
        default=False,
        help="If enabled all performance tests will be skipped.",
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
    if "no_performance_tests" in item.keywords and item.config.getoption("--no-performance-tests"):
        pytest.skip(
            "Skipping performance test because " "--no-performance-tests flag is specified."
        )
