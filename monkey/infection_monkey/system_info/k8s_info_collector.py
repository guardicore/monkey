import logging
import os

from infection_monkey.system_info import InfoCollector
from infection_monkey.system_info.SSH_info_collector import SSHCollector

__author__ = 'uri'

LOG = logging.getLogger(__name__)


class K8sInfoCollector:
    """
    K8s information collecting module for Linux operating systems
    """

    def __init__(self):
        pass

    @staticmethod
    def get_info():
        """
        Collect k8s system information
        :return: Dict of k8s information
        """
        return \
            {
                'is_pod': K8sInfoCollector.is_pod()
            }

    @staticmethod
    def is_pod():
        os.path.exists('/var/run/secrets/kubernetes.io')

