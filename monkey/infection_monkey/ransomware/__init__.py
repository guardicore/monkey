import logging

from infection_monkey.config import WormConfiguration

LOG = logging.getLogger(__name__)


def start_ransomware():
    LOG.info(f"Windows dir configured for encryption is {WormConfiguration.windows_dir_ransom}")
    LOG.info(f"Linux dir configured for encryption is {WormConfiguration.linux_dir_ransom}")
