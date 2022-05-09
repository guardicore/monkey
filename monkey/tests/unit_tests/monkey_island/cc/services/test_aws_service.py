import json
import threading
from typing import Optional
from unittest import TestCase

import pytest

from common.aws import AWSInstance
from monkey_island.cc.services import AWSService
from monkey_island.cc.services.aws_service import filter_instance_data_from_aws_response


class TestAwsService(TestCase):
    def test_filter_instance_data_from_aws_response(self):
        json_response_full = """
        {
            "InstanceInformationList": [
                {
                     "ActivationId": "string",
                     "AgentVersion": "string",
                     "AssociationOverview": {
                        "DetailedStatus": "string",
                        "InstanceAssociationStatusAggregatedCount": {
                           "string" : 6
                        }
                     },
                     "AssociationStatus": "string",
                     "ComputerName": "string",
                     "IamRole": "string",
                     "InstanceId": "string",
                     "IPAddress": "string",
                     "IsLatestVersion": "True",
                     "LastAssociationExecutionDate": 6,
                     "LastPingDateTime": 6,
                     "LastSuccessfulAssociationExecutionDate": 6,
                     "Name": "string",
                     "PingStatus": "string",
                     "PlatformName": "string",
                     "PlatformType": "string",
                     "PlatformVersion": "string",
                     "RegistrationDate": 6,
                     "ResourceType": "string"
                }
            ],
           "NextToken": "string"
        }
        """

        json_response_empty = """
            {
                "InstanceInformationList": [],
                "NextToken": "string"
            }
            """

        self.assertEqual(
            filter_instance_data_from_aws_response(json.loads(json_response_empty)), []
        )
        self.assertEqual(
            filter_instance_data_from_aws_response(json.loads(json_response_full)),
            [{"instance_id": "string", "ip_address": "string", "name": "string", "os": "string"}],
        )


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
def aws_service():
    aws_instance = StubAWSInstance(INSTANCE_ID, REGION, ACCOUNT_ID)
    return AWSService(aws_instance)


def test_instance_id(aws_service):
    assert aws_service.island_aws_instance.instance_id == INSTANCE_ID


def test_region(aws_service):
    assert aws_service.island_aws_instance.region == REGION


def test_account_id(aws_service):
    assert aws_service.island_aws_instance.account_id == ACCOUNT_ID
