from . import InfoCollector

__author__ = 'uri'


class LinuxInfoCollector(InfoCollector):
    """
    System information collecting module for Linux operating systems
    """

    def __init__(self):
        super(LinuxInfoCollector, self).__init__()

    def get_info(self):
        self.get_hostname()
        self.get_process_list()
        return self.info
