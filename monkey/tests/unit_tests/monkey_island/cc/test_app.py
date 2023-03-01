import pytest
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import mock_flask_resource_manager

from monkey_island.cc.app import FlaskDIWrapper
from monkey_island.cc.flask_utils import AbstractResource


def get_mock_resource(name, urls):
    class MockResource(AbstractResource):
        urls = []

        def get(self, something=None):
            pass

    mock = type(name, MockResource.__bases__, dict(MockResource.__dict__))
    mock.urls = urls
    return mock


@pytest.fixture
def resource_manager():
    container = StubDIContainer()
    return mock_flask_resource_manager(container)


def test_duplicate_urls(resource_manager):
    resource = get_mock_resource("res1", ["/url"])

    resource2 = get_mock_resource("res1", ["/new_url", "/url"])

    resource_manager.add_resource(resource)
    with pytest.raises(FlaskDIWrapper.DuplicateURLError):
        resource_manager.add_resource(resource2)


def test_duplicate_urls__parameters(resource_manager):
    resource1 = get_mock_resource("res1", ["/url/<string:param1>"])
    resource2 = get_mock_resource("res2", ["/url/<string:param2>"])

    resource_manager.add_resource(resource1)
    with pytest.raises(FlaskDIWrapper.DuplicateURLError):
        resource_manager.add_resource(resource2)


def test_duplicate_urls__multiple_parameters(resource_manager):
    resource1 = get_mock_resource("res1", ["/url/<string:agent_name>/<string:param>"])
    resource2 = get_mock_resource("res2", ["/url/<int:agent_id>/<string:param>"])

    resource_manager.add_resource(resource1)
    with pytest.raises(FlaskDIWrapper.DuplicateURLError):
        resource_manager.add_resource(resource2)


def test_adding_resources(resource_manager):
    resource = get_mock_resource("res1", ["/url"])

    resource2 = get_mock_resource("res2", ["/different_url", "/another_different"])

    resource3 = get_mock_resource("res3", ["/yet_another/<string:something>"])

    # Following shouldn't raise an exception
    resource_manager.add_resource(resource)
    resource_manager.add_resource(resource2)
    resource_manager.add_resource(resource3)


def test_url_check_slash_stripping__trailing_slash(resource_manager):
    resource = get_mock_resource("res", ["/url"])
    resource2 = get_mock_resource("res2", ["/url/"])

    resource_manager.add_resource(resource)
    with pytest.raises(FlaskDIWrapper.DuplicateURLError):
        resource_manager.add_resource(resource2)


def test_url_check_slash_stripping__path_separation(resource_manager):
    resource3 = get_mock_resource("res3", ["/beef/face"])
    resource4 = get_mock_resource("res4", ["/beefface"])

    # Following shouldn't raise and exception
    resource_manager.add_resource(resource3)
    resource_manager.add_resource(resource4)


def test_trailing_slash_enforcement(resource_manager):
    bad_endpoint = "/beef/face/"
    with pytest.raises(ValueError):
        resource3 = get_mock_resource("res3", [f"{bad_endpoint}"])
        resource_manager.add_resource(resource3)
