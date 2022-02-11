import logging

from common.cloud.aws.aws_instance import AwsInstance
from infection_monkey.telemetry.aws_instance_telem import AwsInstanceTelemetry

logger = logging.getLogger(__name__)


def _running_on_aws(aws_instance: AwsInstance) -> bool:
    return aws_instance.is_instance()


def report_aws_environment():
    logger.info("Collecting AWS info")

    aws_instance = AwsInstance()

    if _running_on_aws(aws_instance):
        logger.info("Machine is an AWS instance")
        AwsInstanceTelemetry({"instance_id": aws_instance.get_instance_id()}).send()
    else:
        logger.info("Machine is NOT an AWS instance")
