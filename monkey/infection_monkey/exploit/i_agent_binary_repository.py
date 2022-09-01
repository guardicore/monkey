import abc
import io

from common import OperatingSystem

# TODO: The Island also has an IAgentBinaryRepository with a totally different interface. At the
#       moment, the Island and Agent have different needs, but at some point we should unify these.


class IAgentBinaryRepository(metaclass=abc.ABCMeta):
    """
    IAgentBinaryRepository provides an interface for other components to access agent binaries.
    Notably, this is used by exploiters during propagation to retrieve the appropriate agent binary
    so that it can be uploaded to a victim and executed.
    """

    @abc.abstractmethod
    def get_agent_binary(
        self, operating_system: OperatingSystem, architecture: str = None
    ) -> io.BytesIO:
        """
        Retrieve the appropriate agent binary from the repository.
        :param operating_system: The name of the operating system on which the agent binary will run
        :param architecture: Reserved
        :return: A file-like object for the requested agent binary
        """
        pass
