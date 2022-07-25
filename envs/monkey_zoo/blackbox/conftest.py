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


def pytest_runtest_setup(item):
    if "skip_powershell_reuse" in item.keywords and item.config.getoption(
        "--skip-powershell-reuse"
    ):
        pytest.skip(
            "Skipping powershell credentials reuse test because "
            "--skip-powershell-cached flag isn't specified."
        )
