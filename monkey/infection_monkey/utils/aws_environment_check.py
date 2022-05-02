import logging

from common.aws.aws_instance import AwsInstance
from infection_monkey.telemetry.aws_instance_telem import AWSInstanceTelemetry
from infection_monkey.telemetry.messengers.legacy_telemetry_messenger_adapter import (
    LegacyTelemetryMessengerAdapter,
)
from infection_monkey.utils.threading import create_daemon_thread

logger = logging.getLogger(__name__)


def _report_aws_environment(telemetry_messenger: LegacyTelemetryMessengerAdapter):
    logger.info("Collecting AWS info")

    aws_instance = AwsInstance()

    if aws_instance.is_instance:
        logger.info("Machine is an AWS instance")
        telemetry_messenger.send_telemetry(AWSInstanceTelemetry(aws_instance.instance_id))
    else:
        logger.info("Machine is NOT an AWS instance")


def run_aws_environment_check(telemetry_messenger: LegacyTelemetryMessengerAdapter):
    logger.info("AWS environment check initiated.")
    aws_environment_thread = create_daemon_thread(
        target=_report_aws_environment, name="AWSEnvironmentThread", args=(telemetry_messenger,)
    )
    aws_environment_thread.start()
