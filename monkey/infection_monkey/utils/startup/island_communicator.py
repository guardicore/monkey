from logging import getLogger

from infection_monkey.control import ControlClient
from infection_monkey.config import WormConfiguration

LOG = getLogger(__name__)


class CommunicatorWithIsland:

    def __init__(self, default_server, tunnel, parent=None):
        self._default_server = default_server
        self._default_server_port = ""
        self._tunnel = tunnel
        self._parent = parent
        if self._default_server:
            if self._default_server not in WormConfiguration.command_servers:
                LOG.debug("Added default server: %s" % self._default_server)
                WormConfiguration.command_servers.insert(0, self._default_server)
            else:
                LOG.debug("Default server: %s is already in command servers list" % self._default_server)

        if not self.set_default_server():
            return
        self.set_default_port_from_server_address(self._default_server)

    def load_configuration_from_island(self):
        ControlClient.wakeup(parent=self._parent)
        ControlClient.load_control_config()

    def set_default_port_from_server_address(self, server_address):
        """
        :param server_address: e.g.: 192.168.1.1:5000
        """
        try:
            self._default_server_port = server_address.split(':')[1]
        except KeyError:
            self._default_server_port = ''

    def set_default_server(self):
        if not ControlClient.find_server(default_tunnel=self._tunnel):
            LOG.info("Monkey couldn't find server. Going down.")
            return False
        self._default_server = WormConfiguration.current_server
        LOG.debug("default server set to: %s" % self._default_server)
        return True
