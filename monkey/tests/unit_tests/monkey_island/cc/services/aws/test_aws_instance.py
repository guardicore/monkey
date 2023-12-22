import pytest

from monkey_island.cc.services.aws.aws_instance import AWSInstance

INSTANCE_ID = "1234"
REGION = "USA"
ACCOUNT_ID = "4321"


@pytest.fixture
def patch_fetch_metadata(monkeypatch):
    def inner(instance_id: str, region: str, account_id: str):
        return_value = (instance_id, region, account_id)
        monkeypatch.setattr(
            "monkey_island.cc.services.aws.aws_instance.fetch_aws_instance_metadata",
            lambda: return_value,
        )

    return inner


@pytest.fixture(autouse=True)
def patch_fetch_metadata_default_values(patch_fetch_metadata):
    patch_fetch_metadata(INSTANCE_ID, REGION, ACCOUNT_ID)


def test_is_instance__true():
    aws_instance = AWSInstance()

    assert aws_instance.is_instance is True


def test_is_instance__false_none(patch_fetch_metadata):
    patch_fetch_metadata(None, "", "")
    aws_instance = AWSInstance()

    assert aws_instance.is_instance is False


def test_is_instance__false_empty_str(patch_fetch_metadata):
    patch_fetch_metadata("", "", "")
    aws_instance = AWSInstance()

    assert aws_instance.is_instance is False


def test_instance_id():
    aws_instance = AWSInstance()

    assert aws_instance.instance_id == INSTANCE_ID


def test_region():
    aws_instance = AWSInstance()

    assert aws_instance.region == REGION


def test_account_id():
    aws_instance = AWSInstance()

    assert aws_instance.account_id == ACCOUNT_ID
