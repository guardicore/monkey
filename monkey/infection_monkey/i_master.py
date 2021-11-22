import abc


class IMaster(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def start(self) -> None:
        """
        With the help of the puppet, starts and instructs the Agent to
        perform various actions like scanning or exploiting a specific host.
        """
        pass

    @abc.abstractmethod
    def terminate(self) -> None:
        """
        Effectively marks the Agent as dead, telling all actions being
        performed by the Agent to stop.
        """
        pass

    @abc.abstractmethod
    def cleanup(self) -> None:
        """
        With the help of the puppet, instructs the Agent to cleanup whatever
        is required since the Agent was killed.
        """
        pass
