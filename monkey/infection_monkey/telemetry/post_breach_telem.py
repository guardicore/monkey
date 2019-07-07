import socket

from infection_monkey.telemetry.base_telem import BaseTelem

__author__ = "itay.mizeretz"


class PostBreachTelem(BaseTelem):

    def __init__(self, pba, result):
        """
        Default post breach telemetry constructor
        :param pba: Post breach action which was used
        :param result: Result of PBA
        """
        super(PostBreachTelem, self).__init__()
        self.pba = pba
        self.result = result
        self.hostname, self.ip = PostBreachTelem._get_hostname_and_ip()

    telem_category = 'post_breach'

    def get_data(self):
        return {
            'command': self.pba.command,
            'result': self.result,
            'name': self.pba.name,
            'hostname': self.hostname,
            'ip': self.ip
        }

    @staticmethod
    def _get_hostname_and_ip():
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        except socket.error:
            hostname = "Unknown"
            ip = "Unknown"
        return hostname, ip
