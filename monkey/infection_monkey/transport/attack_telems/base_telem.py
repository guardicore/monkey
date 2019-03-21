from enum import Enum
from infection_monkey.config import WormConfiguration
import requests
import json
from infection_monkey.control import ControlClient
import logging
from infection_monkey.utils import get_host_info

__author__ = "VakarisZ"

LOG = logging.getLogger(__name__)


class ScanStatus(Enum):
    # Technique wasn't scanned
    UNSCANNED = 0
    # Technique was attempted/scanned
    SCANNED = 1
    # Technique was attempted and succeeded
    USED = 2


class AttackTelem(object):

    def __init__(self, technique, status, data=None, machine=False):
        """
        Default ATT&CK telemetry constructor
        :param technique: Technique ID. E.g. T111
        :param status: int from ScanStatus Enum
        :param data: Other data relevant to the attack technique
        :param machine: Boolean. Should we pass current machine's info or not
        """
        self.technique = technique
        self.result = status
        self.data = {'status': status}
        if data:
            self.data.update(data)
        if machine:
            self.data.update({'machine': get_host_info()})

    def send(self):
        """
        Sends telemetry to island
        :return:
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
