from enum import Enum
from infection_monkey.config import WormConfiguration, GUID
import requests
import json
from infection_monkey.control import ControlClient
import logging

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

    def __init__(self, technique, status, data, machine=None):
        self.technique = technique
        self.result = status
        self.data = {'machine': machine, 'status': status, 'monkey_guid': GUID}
        self.data.update(data)

    def send(self):
        if not WormConfiguration.current_server:
            return
        try:
            reply = requests.post("https://%s/api/%s" % (WormConfiguration.current_server, self.technique),
                                  data=json.dumps(self.data),
                                  headers={'content-type': 'application/json'},
                                  verify=False,
                                  proxies=ControlClient.proxies)
        except Exception as exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)
