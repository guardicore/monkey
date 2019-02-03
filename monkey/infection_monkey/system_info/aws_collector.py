import logging

from common.cloud.aws import AWS

__author__ = 'itay.mizeretz'

LOG = logging.getLogger(__name__)


class AwsCollector(object):
    """
    Extract info from AWS machines
    """

    @staticmethod
    def get_aws_info():
        LOG.info("Collecting AWS info")
        aws = AWS()
        info = {}
        if aws.is_aws_instance():
            LOG.info("Machine is an AWS instance")
            info = \
                {
                    'instance_id': aws.get_instance_id()
                }
        else:
            LOG.info("Machine is NOT an AWS instance")

        return info
