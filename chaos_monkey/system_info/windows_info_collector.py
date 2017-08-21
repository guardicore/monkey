from . import InfoCollector
from mimikatz_collector import MimikatzCollector
__author__ = 'uri'


class WindowsInfoCollector(InfoCollector):
    """
    System information collecting module for Windows operating systems
    """

    def __init__(self):
        super(WindowsInfoCollector, self).__init__()

    def get_info(self):
        self.get_hostname()
        self.get_process_list()
        mimikatz_collector = MimikatzCollector()
        self.info["credentials"] = mimikatz_collector.get_logon_info()
        return self.info
