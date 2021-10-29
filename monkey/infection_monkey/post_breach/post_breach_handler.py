import logging
from multiprocessing.dummy import Pool
from typing import Sequence

from infection_monkey.post_breach.pba import PBA

logger = logging.getLogger(__name__)


class PostBreach(object):
    """
    This class handles post breach actions execution
    """

    def __init__(self):
        self.pba_list = self.config_to_pba_list()

    def execute_all_configured(self):
        """
        Executes all post breach actions.
        """
        with Pool(5) as pool:
            pool.map(self.run_pba, self.pba_list)
            logger.info("All PBAs executed. Total {} executed.".format(len(self.pba_list)))

    @staticmethod
    def config_to_pba_list() -> Sequence[PBA]:
        """
        :return: A list of PBA objects.
        """
        return PBA.get_instances()

    def run_pba(self, pba):
        try:
            logger.debug("Executing PBA: '{}'".format(pba.name))
            pba.run()
            logger.debug(f"Execution of {pba.name} finished")
        except Exception as e:
            logger.error("PBA {} failed. Error info: {}".format(pba.name, e))
