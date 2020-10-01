import logging

from common.cloud.aws.aws_instance import AwsInstance
from common.cloud.scoutsuite_consts import PROVIDERS
from common.common_consts.system_info_collectors_names import AWS_COLLECTOR
from common.network.network_utils import is_running_on_island
from infection_monkey.system_info.collectors.scoutsuite_collector.scoutsuite_collector import scan_cloud_security
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
        if is_running_on_island():
            logger.info("Attempting to scan AWS security with ScoutSuite.")
            scan_cloud_security(cloud_type=PROVIDERS.AWS)
        else:
            logger.info("Didn't scan AWS security with ScoutSuite, because not on island.")
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
