import json
from unittest import TestCase

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
