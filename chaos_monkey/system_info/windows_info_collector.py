import socket
__author__ = 'uri'


class WindowsInfoCollector(object):
    """
    System information collecting module for Windows operating systems
    """

    def __init__(self):
        self.info = {}

    def collect(self):
        self.info['hostname'] = socket.gethostname()

    def get_info(self):
        self.collect()
        return self.info
