import threading
from typing import Any, Dict, Optional, Sequence

import pytest

from monkey_island.cc.services import AWSService
from monkey_island.cc.services.aws.aws_instance import AWSInstance

EXPECTED_INSTANCE_1 = {
    "instance_id": "1",
    "name": "comp1",
    "os": "linux",
    "ip_address": "192.168.1.1",
}
EXPECTED_INSTANCE_2 = {
    "instance_id": "2",
    "name": "comp2",
    "os": "linux",
    "ip_address": "192.168.1.2",
}

EMPTY_INSTANCE_INFO_RESPONSE = []
FULL_INSTANCE_INFO_RESPONSE = [
    {
        "ActivationId": "string",
        "AgentVersion": "string",
        "AssociationOverview": {
            "DetailedStatus": "string",
            "InstanceAssociationStatusAggregatedCount": {"string": 6},
        },
        "AssociationStatus": "string",
        "ComputerName": EXPECTED_INSTANCE_1["name"],
        "IamRole": "string",
        "InstanceId": EXPECTED_INSTANCE_1["instance_id"],
        "IPAddress": EXPECTED_INSTANCE_1["ip_address"],
        "IsLatestVersion": "True",
        "LastAssociationExecutionDate": 6,
        "LastPingDateTime": 6,
        "LastSuccessfulAssociationExecutionDate": 6,
        "Name": "string",
        "PingStatus": "string",
        "PlatformName": "string",
        "PlatformType": EXPECTED_INSTANCE_1["os"],
        "PlatformVersion": "string",
        "RegistrationDate": 6,
        "ResourceType": "string",
    },
    {
        "ActivationId": "string",
        "AgentVersion": "string",
        "AssociationOverview": {
            "DetailedStatus": "string",
            "InstanceAssociationStatusAggregatedCount": {"string": 6},
        },
        "AssociationStatus": "string",
        "ComputerName": EXPECTED_INSTANCE_2["name"],
        "IamRole": "string",
        "InstanceId": EXPECTED_INSTANCE_2["instance_id"],
        "IPAddress": EXPECTED_INSTANCE_2["ip_address"],
        "IsLatestVersion": "True",
        "LastAssociationExecutionDate": 6,
        "LastPingDateTime": 6,
        "LastSuccessfulAssociationExecutionDate": 6,
        "Name": "string",
        "PingStatus": "string",
        "PlatformName": "string",
        "PlatformType": EXPECTED_INSTANCE_2["os"],
        "PlatformVersion": "string",
        "RegistrationDate": 6,
        "ResourceType": "string",
    },
]


class StubAWSInstance(AWSInstance):
    def __init__(
        self,
        instance_id: Optional[str] = None,
        region: Optional[str] = None,
        account_id: Optional[str] = None,
    ):
        self._instance_id = instance_id
        self._region = region
        self._account_id = account_id

        self._initialization_complete = threading.Event()
        self._initialization_complete.set()


def test_aws_is_on_aws__true():
    aws_instance = StubAWSInstance("1")
    aws_service = AWSService(aws_instance)
    assert aws_service.island_is_running_on_aws() is True


def test_aws_is_on_aws__False():
    aws_instance = StubAWSInstance()
    aws_service = AWSService(aws_instance)
    assert aws_service.island_is_running_on_aws() is False


INSTANCE_ID = "1"
REGION = "2"
ACCOUNT_ID = "3"


@pytest.fixture
def aws_instance():
    return StubAWSInstance(INSTANCE_ID, REGION, ACCOUNT_ID)


@pytest.fixture
def aws_service(aws_instance):
    return AWSService(aws_instance)


def test_instance_id(aws_service):
    assert aws_service.island_aws_instance.instance_id == INSTANCE_ID


def test_region(aws_service):
    assert aws_service.island_aws_instance.region == REGION


def test_account_id(aws_service):
    assert aws_service.island_aws_instance.account_id == ACCOUNT_ID


class MockAWSService(AWSService):
    def __init__(self, aws_instance: AWSInstance, instance_info_response: Sequence[Dict[str, Any]]):
        super().__init__(aws_instance)
        self._instance_info_response = instance_info_response

    def _get_raw_managed_instances(self):
        return self._instance_info_response


def test_get_managed_instances__empty(aws_instance):
    aws_service = MockAWSService(aws_instance, EMPTY_INSTANCE_INFO_RESPONSE)
    instances = aws_service.get_managed_instances()
    assert len(instances) == 0


def test_get_managed_instances(aws_instance):
    aws_service = MockAWSService(aws_instance, FULL_INSTANCE_INFO_RESPONSE)
    instances = aws_service.get_managed_instances()

    assert len(instances) == 2
    assert instances[0] == EXPECTED_INSTANCE_1
    assert instances[1] == EXPECTED_INSTANCE_2
