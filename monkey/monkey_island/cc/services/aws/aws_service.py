import logging
from typing import Any, Iterable, Mapping, Sequence

import boto3
import botocore

from common.aws.aws_instance import AWSInstance

INSTANCE_INFORMATION_LIST_KEY = "InstanceInformationList"
INSTANCE_ID_KEY = "InstanceId"
COMPUTER_NAME_KEY = "ComputerName"
PLATFORM_TYPE_KEY = "PlatformType"
IP_ADDRESS_KEY = "IPAddress"

logger = logging.getLogger(__name__)


class AWSService:
    def __init__(self, aws_instance: AWSInstance):
        """
        :param aws_instance: An AWSInstance object representing the AWS instance that the Island is
                             running on
        """
        self._aws_instance = aws_instance

    def island_is_running_on_aws(self) -> bool:
        """
        :return: True if the island is running on an AWS instance. False otherwise.
        :rtype: bool
        """
        return self._aws_instance.is_instance

    @property
    def island_aws_instance(self) -> AWSInstance:
        """
        :return: an AWSInstance object representing the AWS instance that the Island is running on.
        :rtype: AWSInstance
        """
        return self._aws_instance

    def get_managed_instances(self) -> Sequence[Mapping[str, str]]:
        """
        :return: A sequence of mappings, where each Mapping represents a managed AWS instance that
                 is accessible from the Island.
        :rtype: Sequence[Mapping[str, str]]
        """
        raw_managed_instances_info = self._get_raw_managed_instances()
        return _filter_relevant_instance_info(raw_managed_instances_info)

    def _get_raw_managed_instances(self) -> Sequence[Mapping[str, Any]]:
        """
        Get the information for all instances with the relevant roles.

        This function will assume that it's running on an EC2 instance with the correct IAM role.
        See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#iam
        -role for details.

        :raises: botocore.exceptions.ClientError if can't describe local instance information.
        :return: All visible instances from this instance
        """
        ssm_client = boto3.client("ssm", self.island_aws_instance.region)
        try:
            response = ssm_client.describe_instance_information()
            return response[INSTANCE_INFORMATION_LIST_KEY]
        except botocore.exceptions.ClientError as err:
            logger.warning("AWS client error while trying to get manage dinstances: {err}")
            raise err

    def run_agent_on_managed_instances(self, instance_ids: Iterable[str]):
        for id_ in instance_ids:
            self._run_agent_on_managed_instance(id_)

    def _run_agent_on_managed_instance(self, instance_id: str):
        pass


def _filter_relevant_instance_info(raw_managed_instances_info: Sequence[Mapping[str, Any]]):
    """
    Consume raw instance data from the AWS API and return only those fields that are relevant for
    Infection Monkey.

    :param raw_managed_instances_info: The output of
                                       DescribeInstanceInformation["InstanceInformation"] from the
                                       AWS API
    :return: A sequence of mappings, where each Mapping represents a managed AWS instance that
             is accessible from the Island.
    :rtype: Sequence[Mapping[str, str]]
    """
    return [
        {
            "instance_id": managed_instance[INSTANCE_ID_KEY],
            "name": managed_instance[COMPUTER_NAME_KEY],
            "os": managed_instance[PLATFORM_TYPE_KEY].lower(),
            "ip_address": managed_instance[IP_ADDRESS_KEY],
        }
        for managed_instance in raw_managed_instances_info
    ]
