from typing import Optional

from monkeytypes import OperatingSystem
from pymongo import MongoClient

from monkey_island.cc.repositories import RemovalError, RetrievalError, StorageError
from monkey_island.cc.repositories.consts import MONGO_OBJECT_ID_KEY

from .i_masquerade_repository import IMasqueradeRepository


class MongoMasqueradeRepository(IMasqueradeRepository):
    """
    Store the masques that are to be applied to the Agent binaries in a mongo database.
    """

    def __init__(self, mongo: MongoClient):
        self._collection = mongo.monkey_island.masques

    def get_masque(self, operating_system: OperatingSystem) -> Optional[bytes]:
        try:
            masque_document = self._collection.find_one(
                {"operating_system": operating_system.value}, {MONGO_OBJECT_ID_KEY: False}
            )
            return masque_document["masque"] if masque_document else None
        except Exception as err:
            raise RetrievalError(f"Error retrieving {operating_system.value} masque: {err}")

    def set_masque(self, operating_system: OperatingSystem, masque: Optional[bytes]):
        try:
            self._collection.replace_one(
                {"operating_system": operating_system.value},
                {"operating_system": operating_system.value, "masque": masque},
                upsert=True,
            )
        except Exception as err:
            raise StorageError(f"Error updating {operating_system.value} masque: {err}")

    def reset(self):
        try:
            self._collection.drop()
        except Exception as err:
            raise RemovalError(f"Error removing masques: {err}")
