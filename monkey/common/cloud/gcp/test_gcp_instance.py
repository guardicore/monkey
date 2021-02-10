import pytest
import requests
import requests_mock

from common.cloud.environment_names import Environment
from common.cloud.gcp.gcp_instance import GCP_METADATA_SERVICE_URL, GcpInstance


def get_test_gcp_instance(url, **kwargs):
    with requests_mock.Mocker() as m:
        m.get(url, **kwargs)
        test_gcp_instance_object = GcpInstance()
        return test_gcp_instance_object


# good request
@pytest.fixture
def good_request_mock_instance():
    return get_test_gcp_instance(GCP_METADATA_SERVICE_URL)


def test_is_instance_good_request(good_request_mock_instance):
    assert good_request_mock_instance.is_instance()


def test_get_cloud_provider_name_good_request(good_request_mock_instance):
    assert good_request_mock_instance.get_cloud_provider_name() == Environment.GCP


# bad request
@pytest.fixture
def bad_request_mock_instance():
    return get_test_gcp_instance(GCP_METADATA_SERVICE_URL, exc=requests.RequestException)


def test_is_instance_bad_request(bad_request_mock_instance):
    assert bad_request_mock_instance.is_instance() is False


def test_get_cloud_provider_name_bad_request(bad_request_mock_instance):
    assert bad_request_mock_instance.get_cloud_provider_name() == Environment.GCP


# not found request
@pytest.fixture
def not_found_request_mock_instance():
    return get_test_gcp_instance(GCP_METADATA_SERVICE_URL, status_code=404)


def test_is_instance_not_found_request(not_found_request_mock_instance):
    assert not_found_request_mock_instance.is_instance() is False


def test_get_cloud_provider_name_not_found_request(not_found_request_mock_instance):
    assert not_found_request_mock_instance.get_cloud_provider_name() == Environment.GCP
