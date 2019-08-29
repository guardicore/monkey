import pytest


def pytest_addoption(parser):
    parser.addoption("--island", action="store", default="",
                     help="Specify the Monkey Island address (host+port).")


@pytest.fixture
def island(request):
    request.cls.island = request.config.getoption("--island")
