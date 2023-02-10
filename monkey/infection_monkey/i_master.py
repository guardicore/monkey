import abc


class IMaster(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def start(self) -> None:
        """
        Run the control logic that will instruct the Puppet to perform various actions like scanning
        or exploiting a specific host.
        """

    @abc.abstractmethod
    def terminate(self, block: bool = False) -> None:
        """
        Stop the master and interrupt any actions that are currently being executed.
        :param bool block: Whether or not to block and wait for the master to terminate.
        """

    @abc.abstractmethod
    def cleanup(self) -> None:
        """
        Revert any changes that the master has directly or indirectly caused to the system.
        """
