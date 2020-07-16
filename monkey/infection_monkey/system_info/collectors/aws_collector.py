import logging

from common.cloud.aws.aws_instance import AwsInstance
from common.data.system_info_collectors_names import AWS_COLLECTOR
from infection_monkey.system_info.system_info_collector import \
    SystemInfoCollector

logger = logging.getLogger(__name__)


class AwsCollector(SystemInfoCollector):
    """
    Extract info from AWS machines.
    """
    def __init__(self):
        super().__init__(name=AWS_COLLECTOR)

    def collect(self) -> dict:
        logger.info("Collecting AWS info")
        aws = AwsInstance()
        info = {}
        if aws.is_instance():
            logger.info("Machine is an AWS instance")
            info = \
                {
                    'instance_id': aws.get_instance_id()
                }
        else:
            logger.info("Machine is NOT an AWS instance")

        return info
