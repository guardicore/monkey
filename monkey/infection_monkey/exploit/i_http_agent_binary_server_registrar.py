import abc
from ipaddress import IPv4Address

from common import OperatingSystem

from .http_agent_binary_server import AgentBinaryDownloadTicket, AgentBinaryTransform, ReservationID


class IHTTPAgentBinaryServerRegistrar(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def reserve_download(
        self,
        operating_system: OperatingSystem,
        requestor_ip: IPv4Address,
        agent_binary_transform: AgentBinaryTransform,
    ) -> AgentBinaryDownloadTicket:
        """
        Register to download an Agent over HTTP

        :param operating_system: The operating system for the Agent binary to serve
        :param requestor_ip: The IP address of the client that will download the Agent binary
        :param agent_binary_transform: A function that transforms the Agent binary before serving
        :raises RuntimeError: If the binary could not be served
        :returns: A ticket to download the Agent binary
        """
        pass

    @abc.abstractmethod
    def clear_reservation(self, reservation_id: ReservationID):
        """
        Deregister a AgentBinaryDownloadReservation from the registrar

        :param reservation_id: The ID of the reservation to be deregistered
        :raises KeyError: If the reservation ID is not registered
        """
        pass
