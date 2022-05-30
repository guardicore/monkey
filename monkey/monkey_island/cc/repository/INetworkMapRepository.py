from abc import ABC


class INetworkMapRepository(ABC):

    # TODO Define NetMap object
    def get_map(self) -> NetMap:  # noqa: F821
        pass

    def save_netmap(self, netmap: NetMap):  # noqa: F821
        pass
