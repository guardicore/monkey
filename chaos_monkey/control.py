
import json
import random
import logging
import requests
from config import WormConfiguration

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

class ControlClient(object):
    @staticmethod
    def get_control_config():
        try:
            reply = requests.get("http://%s/orders/%s" % (WormConfiguration.command_server,
                                                          "".join([chr(random.randint(0,255)) for _ in range(32)]).encode("base64").strip()))


        except Exception, exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.command_server, exc)
            return {}

        try:
            return json.loads(reply._content)
        except ValueError, exc:
            LOG.warn("Error parsing JSON reply from control server %s (%s): %s",
                     WormConfiguration.command_server, reply._content, exc)
            return {}

