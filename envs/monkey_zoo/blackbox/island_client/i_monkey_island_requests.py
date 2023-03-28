from abc import ABC, abstractmethod
from typing import Dict


class IMonkeyIslandRequests(ABC):
    @abstractmethod
    def get_token_from_server(self):
        pass

    @abstractmethod
    def get(self, url, data=None):
        pass

    @abstractmethod
    def post(self, url, data):
        pass

    @abstractmethod
    def put(self, url, data):
        pass

    @abstractmethod
    def put_json(self, url, json: Dict):
        pass

    @abstractmethod
    def post_json(self, url, json: Dict):
        pass

    @abstractmethod
    def patch(self, url, data: Dict):
        pass

    @abstractmethod
    def delete(self, url):
        pass
