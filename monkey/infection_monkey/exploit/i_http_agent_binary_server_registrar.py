import abc
from ipaddress import IPv4Address

from common import OperatingSystem

from .http_agent_binary_server import AgentBinaryDownloadTicket, AgentBinaryTransform, ReservationID


class IHTTPAgentBinaryServerRegistrar(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def register_request(
        self,
        operating_system: OperatingSystem,
        requestor_ip: IPv4Address,
        agent_binary_transform: AgentBinaryTransform,
    ) -> AgentBinaryDownloadTicket:
        """
        Registers an Agent to be served with HTTPAgentBinaryServer

        :param operating_system: The operating system for the Agent binary to serve
        :param requestor_ip: The IP address of the client that will download the Agent binary
        :param agent_binary_transform: A function that transforms the Agent binary before serving
        :raises RuntimeError: If the binary could not be served
        :returns: A ticket to download the Agent binary
        """
        pass

    @abc.abstractmethod
    def deregister_request(self, reservation_id: ReservationID):
        """
        Deregister a AgentBinaryDownloadReservation from the registrar

        :param reservation_id: The ID of the request to be deregistered
        :raises KeyError: If the request ID is not registered
        """
        pass
