import logging
from functools import wraps
from threading import Event
from typing import Callable, Optional

import boto3
import botocore

from common.aws.aws_instance import AwsInstance

INSTANCE_INFORMATION_LIST_KEY = "InstanceInformationList"
INSTANCE_ID_KEY = "InstanceId"
COMPUTER_NAME_KEY = "ComputerName"
PLATFORM_TYPE_KEY = "PlatformType"
IP_ADDRESS_KEY = "IPAddress"

logger = logging.getLogger(__name__)


def filter_instance_data_from_aws_response(response):
    return [
        {
            "instance_id": x[INSTANCE_ID_KEY],
            "name": x[COMPUTER_NAME_KEY],
            "os": x[PLATFORM_TYPE_KEY].lower(),
            "ip_address": x[IP_ADDRESS_KEY],
        }
        for x in response[INSTANCE_INFORMATION_LIST_KEY]
    ]


aws_instance: Optional[AwsInstance] = None
AWS_INFO_FETCH_TIMEOUT = 10.0  # Seconds
init_done = Event()


def initialize():
    global aws_instance
    aws_instance = AwsInstance()
    init_done.set()


def wait_init_done(fnc: Callable):
    @wraps(fnc)
    def inner():
        awaited = init_done.wait(AWS_INFO_FETCH_TIMEOUT)
        if not awaited:
            logger.error(
                f"AWS service couldn't initialize in time! "
                f"Current timeout is {AWS_INFO_FETCH_TIMEOUT}, "
                f"but AWS info took longer to fetch from metadata server."
            )
            return
        fnc()

    return inner


@wait_init_done
def is_on_aws():
    return aws_instance.is_instance


@wait_init_done
def get_region():
    return aws_instance.region


@wait_init_done
def get_account_id():
    return aws_instance.account_id


@wait_init_done
def get_client(client_type):
    return boto3.client(client_type, region_name=aws_instance.region)


@wait_init_done
def get_instances():
    """
    Get the information for all instances with the relevant roles.

    This function will assume that it's running on an EC2 instance with the correct IAM role.
    See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#iam
    -role for details.

    :raises: botocore.exceptions.ClientError if can't describe local instance information.
    :return: All visible instances from this instance
    """
    local_ssm_client = boto3.client("ssm", aws_instance.region)
    try:
        response = local_ssm_client.describe_instance_information()

        filtered_instances_data = filter_instance_data_from_aws_response(response)
        return filtered_instances_data
    except botocore.exceptions.ClientError as e:
        logger.warning("AWS client error while trying to get instances: " + e)
        raise e
