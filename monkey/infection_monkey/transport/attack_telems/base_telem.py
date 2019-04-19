from infection_monkey.config import WormConfiguration, GUID
import requests
import json
from infection_monkey.control import ControlClient
import logging

__author__ = "VakarisZ"

LOG = logging.getLogger(__name__)


class AttackTelem(object):

    def __init__(self, technique, status, data=None):
        """
        Default ATT&CK telemetry constructor
        :param technique: Technique ID. E.g. T111
        :param status: int from ScanStatus Enum
        :param data: Dictionary of other relevant info. E.g. {'brute_force_blocked': True}
        """
        self.technique = technique
        self.result = status
        self.data = {'status': status, 'id': GUID}
        if data:
            self.data.update(data)

    def send(self):
        """
        Sends telemetry to island
        """
        if not WormConfiguration.current_server:
            return
        try:
            requests.post("https://%s/api/attack/%s" % (WormConfiguration.current_server, self.technique),
                          data=json.dumps(self.data),
                          headers={'content-type': 'application/json'},
                          verify=False,
                          proxies=ControlClient.proxies)
        except Exception as exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)
