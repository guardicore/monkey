import logging
from typing import Sequence

from infection_monkey.post_breach.pba import PBA
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'

PATH_TO_ACTIONS = "infection_monkey.post_breach.actions."


class PostBreach(object):
    """
    This class handles post breach actions execution
    """

    def __init__(self):
        self.os_is_linux = not is_windows_os()
        self.pba_list = self.config_to_pba_list()

    def execute_all_configured(self):
        """
        Executes all post breach actions.
        """
        for pba in self.pba_list:
            try:
                LOG.debug("Executing PBA: '{}'".format(pba.name))
                pba.run()
            except Exception as e:
                LOG.error("PBA {} failed. Error info: {}".format(pba.name, e))
        LOG.info("All PBAs executed. Total {} executed.".format(len(self.pba_list)))

    @staticmethod
    def config_to_pba_list() -> Sequence[PBA]:
        """
        :return: A list of PBA objects.
        """
        return PBA.get_instances()
