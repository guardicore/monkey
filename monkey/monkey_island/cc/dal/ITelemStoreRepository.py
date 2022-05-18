from abc import ABC


class ITelemStoreRepository(ABC):
    def get_telemetries(self):
        # Used to get ExportedTelem for the Telemtry Store
        pass
