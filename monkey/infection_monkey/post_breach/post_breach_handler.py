import logging
import inspect
import importlib
from infection_monkey.post_breach.pba import PBA
from infection_monkey.post_breach.actions import get_pba_files
from infection_monkey.utils import is_windows_os

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

    def execute(self):
        """
        Executes all post breach actions.
        """
        for pba in self.pba_list:
            pba.run()
        LOG.info("Post breach actions executed")

    @staticmethod
    def config_to_pba_list():
        """
        Passes config to each post breach action class and aggregates results into a list.
        :return: A list of PBA objects.
        """
        pba_list = []
        pba_files = get_pba_files()
        # Go through all of files in ./actions
        for pba_file in pba_files:
            # Import module from that file
            module = importlib.import_module(PATH_TO_ACTIONS + pba_file)
            # Get all classes in a module
            pba_classes = [m[1] for m in inspect.getmembers(module, inspect.isclass)
                           if ((m[1].__module__ == module.__name__) and issubclass(m[1], PBA))]
            # Get post breach action object from class
            for pba_class in pba_classes:
                if pba_class.should_run(pba_class.__name__):
                    pba = pba_class()
                    pba_list.append(pba)
        return pba_list
