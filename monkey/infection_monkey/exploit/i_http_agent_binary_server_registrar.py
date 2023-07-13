import abc
from ipaddress import IPv4Address
from pathlib import PurePath
from typing import Optional, Sequence

from common import OperatingSystem

from .http_agent_binary_server import AgentBinaryDownloadTicket, RequestID, RequestType


class IHTTPAgentBinaryServerRegistrar(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def register_request(
        self,
        operating_system: OperatingSystem,
        request_type: RequestType,
        requestor_ip: IPv4Address,
        destination_path: Optional[PurePath],
        args: Sequence[str],
    ) -> AgentBinaryDownloadTicket:
        """
        Registers an Agent to be served with HTTPAgentBinaryServer

        :param operating_system: The operating system for the Agent binary to serve
        :param request_type: The type of request to serve
        :param requestor_ip: The IP address of the client that will download the Agent binary
        :param destination_path: The destination path into which to drop the Agent binary. This
            only applies to the dropper script request type
        :param args: The arguments to pass to the Agent binary. This only applies to the dropper
            script request type
        :raises RuntimeError: If the binary could not be served
        :returns: A ticket to download the Agent binary
        """
        pass

    @abc.abstractmethod
    def deregister_request(self, request_id: RequestID):
        """
        Deregister a AgentBinaryDownloadReservation from the registrar

        :param request_id: The ID of the request to be deregistered
        :raises KeyError: If the request ID is not registered
        """
        pass
