from types import MappingProxyType

import pytest
import requests
import requests_mock

from common.aws.aws_instance import AWS_LATEST_METADATA_URI_PREFIX, AwsInstance

INSTANCE_ID_RESPONSE = "i-1234567890abcdef0"

AVAILABILITY_ZONE_RESPONSE = "us-west-2b"

# from https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html
INSTANCE_IDENTITY_DOCUMENT_RESPONSE = """
{
    "devpayProductCodes": null,
    "marketplaceProductCodes": ["1abc2defghijklm3nopqrs4tu"],
    "availabilityZone": "us-west-2b",
    "privateIp": "10.158.112.84",
    "version": "2017-09-30",
    "instanceId": "i-1234567890abcdef0",
    "billingProducts": null,
    "instanceType": "t2.micro",
    "accountId": "123456789012",
    "imageId": "ami-5fb8c835",
    "pendingTime": "2016-11-19T16:32:11Z",
    "architecture": "x86_64",
    "kernelId": null,
    "ramdiskId": null,
    "region": "us-west-2"
}
"""

EXPECTED_INSTANCE_ID = "i-1234567890abcdef0"

EXPECTED_REGION = "us-west-2"

EXPECTED_ACCOUNT_ID = "123456789012"


def get_test_aws_instance(
    text=MappingProxyType({"instance_id": None, "region": None, "account_id": None}),
    exception=MappingProxyType({"instance_id": None, "region": None, "account_id": None}),
):
    with requests_mock.Mocker() as m:
        # request made to get instance_id
        url = f"{AWS_LATEST_METADATA_URI_PREFIX}meta-data/instance-id"
        m.get(url, text=text["instance_id"]) if text["instance_id"] else m.get(
            url, exc=exception["instance_id"]
        )

        # request made to get region
        url = f"{AWS_LATEST_METADATA_URI_PREFIX}meta-data/placement/availability-zone"
        m.get(url, text=text["region"]) if text["region"] else m.get(url, exc=exception["region"])

        # request made to get account_id
        url = f"{AWS_LATEST_METADATA_URI_PREFIX}dynamic/instance-identity/document"
        m.get(url, text=text["account_id"]) if text["account_id"] else m.get(
            url, exc=exception["account_id"]
        )

        test_aws_instance_object = AwsInstance()
        return test_aws_instance_object


# all good data
@pytest.fixture
def good_data_mock_instance():
    instance = get_test_aws_instance(
        text={
            "instance_id": INSTANCE_ID_RESPONSE,
            "region": AVAILABILITY_ZONE_RESPONSE,
            "account_id": INSTANCE_IDENTITY_DOCUMENT_RESPONSE,
        }
    )
    yield instance
    del instance


def test_is_instance_good_data(good_data_mock_instance):
    assert good_data_mock_instance.is_instance


def test_instance_id_good_data(good_data_mock_instance):
    assert good_data_mock_instance.instance_id == EXPECTED_INSTANCE_ID


def test_region_good_data(good_data_mock_instance):
    assert good_data_mock_instance.region == EXPECTED_REGION


def test_account_id_good_data(good_data_mock_instance):
    assert good_data_mock_instance.account_id == EXPECTED_ACCOUNT_ID


# 'region' bad data
@pytest.fixture
def bad_region_data_mock_instance():
    instance = get_test_aws_instance(
        text={
            "instance_id": INSTANCE_ID_RESPONSE,
            "region": "in-a-different-world",
            "account_id": INSTANCE_IDENTITY_DOCUMENT_RESPONSE,
        }
    )
    yield instance
    del instance


def test_is_instance_bad_region_data(bad_region_data_mock_instance):
    assert bad_region_data_mock_instance.is_instance


def test_instance_id_bad_region_data(bad_region_data_mock_instance):
    assert bad_region_data_mock_instance.instance_id == EXPECTED_INSTANCE_ID


def test_region_bad_region_data(bad_region_data_mock_instance):
    assert bad_region_data_mock_instance.region is None


def test_account_id_bad_region_data(bad_region_data_mock_instance):
    assert bad_region_data_mock_instance.account_id == EXPECTED_ACCOUNT_ID


# 'account_id' bad data
@pytest.fixture
def bad_account_id_data_mock_instance():
    instance = get_test_aws_instance(
        text={
            "instance_id": INSTANCE_ID_RESPONSE,
            "region": AVAILABILITY_ZONE_RESPONSE,
            "account_id": "who-am-i",
        }
    )
    yield instance
    del instance


def test_is_instance_bad_account_id_data(bad_account_id_data_mock_instance):
    assert not bad_account_id_data_mock_instance.is_instance


def test_instance_id_bad_account_id_data(bad_account_id_data_mock_instance):
    assert bad_account_id_data_mock_instance.instance_id is None


def test_region_bad_account_id_data(bad_account_id_data_mock_instance):
    assert bad_account_id_data_mock_instance.region is None


def test_account_id_data_bad_account_id_data(bad_account_id_data_mock_instance):
    assert bad_account_id_data_mock_instance.account_id is None


# 'region' bad requests
@pytest.fixture
def bad_region_request_mock_instance(region_exception):
    instance = get_test_aws_instance(
        text={
            "instance_id": INSTANCE_ID_RESPONSE,
            "region": None,
            "account_id": INSTANCE_IDENTITY_DOCUMENT_RESPONSE,
        },
        exception={"instance_id": None, "region": region_exception, "account_id": None},
    )
    yield instance
    del instance


@pytest.mark.parametrize("region_exception", [requests.RequestException, IOError])
def test_is_instance_bad_region_request(bad_region_request_mock_instance):
    assert not bad_region_request_mock_instance.is_instance


@pytest.mark.parametrize("region_exception", [requests.RequestException, IOError])
def test_instance_id_bad_region_request(bad_region_request_mock_instance):
    assert bad_region_request_mock_instance.instance_id is None


@pytest.mark.parametrize("region_exception", [requests.RequestException, IOError])
def test_region_bad_region_request(bad_region_request_mock_instance):
    assert bad_region_request_mock_instance.region is None


@pytest.mark.parametrize("region_exception", [requests.RequestException, IOError])
def test_account_id_bad_region_request(bad_region_request_mock_instance):
    assert bad_region_request_mock_instance.account_id is None


# not found request
@pytest.fixture
def not_found_request_mock_instance():
    with requests_mock.Mocker() as m:
        # request made to get instance_id
        url = f"{AWS_LATEST_METADATA_URI_PREFIX}meta-data/instance-id"
        m.get(url, status_code=404)

        # request made to get region
        url = f"{AWS_LATEST_METADATA_URI_PREFIX}meta-data/placement/availability-zone"
        m.get(url)

        # request made to get account_id
        url = f"{AWS_LATEST_METADATA_URI_PREFIX}dynamic/instance-identity/document"
        m.get(url)

        not_found_aws_instance_object = AwsInstance()
        yield not_found_aws_instance_object
        del not_found_aws_instance_object


def test_is_instance_not_found_request(not_found_request_mock_instance):
    assert not_found_request_mock_instance.is_instance is False


def test_instance_id_not_found_request(not_found_request_mock_instance):
    assert not_found_request_mock_instance.instance_id is None


def test_region_not_found_request(not_found_request_mock_instance):
    assert not_found_request_mock_instance.region is None


def test_account_id_not_found_request(not_found_request_mock_instance):
    assert not_found_request_mock_instance.account_id is None
