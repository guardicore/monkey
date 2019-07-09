from infection_monkey.control import ControlClient
from infection_monkey.telemetry.base_telem import BaseTelem

__author__ = "itay.mizeretz"


class TunnelTelem(BaseTelem):

    def __init__(self):
        """
        Default tunnel telemetry constructor
        """
        super(TunnelTelem, self).__init__()
        self.proxy = ControlClient.proxies.get('https')

    telem_category = 'tunnel'

    def get_data(self):
        return {'proxy': self.proxy}
