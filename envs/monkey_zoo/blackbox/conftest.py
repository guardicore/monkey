import pytest


def pytest_addoption(parser):
    parser.addoption("--island", action="store", default="",
                     help="Specify the Monkey Island address (host+port).")


@pytest.fixture(scope='module')
def island(request):
    return request.config.getoption("--island")
