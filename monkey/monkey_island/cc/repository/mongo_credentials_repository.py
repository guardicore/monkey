from typing import Sequence

from pymongo import MongoClient

from common.credentials import Credentials
from monkey_island.cc.repository import RemovalError, RetrievalError, StorageError
from monkey_island.cc.repository.i_credentials_repository import ICredentialsRepository


class MongoCredentialsRepository(ICredentialsRepository):
    """
    Store credentials in a mongo database that can be used to propagate around the network.
    """

    def __init__(self, mongo: MongoClient):
        self._mongo = mongo

    def get_configured_credentials(self) -> Sequence[Credentials]:
        return MongoCredentialsRepository._get_credentials_from_collection(
            self._mongo.db.configured_credentials
        )

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        return MongoCredentialsRepository._get_credentials_from_collection(
            self._mongo.db.stolen_credentials
        )

    def get_all_credentials(self) -> Sequence[Credentials]:
        configured_credentials = self.get_configured_credentials()
        stolen_credentials = self.get_stolen_credentials()

        return [*configured_credentials, *stolen_credentials]

    def save_configured_credentials(self, credentials: Sequence[Credentials]):
        # TODO: Fix deduplication of Credentials in mongo
        MongoCredentialsRepository._save_credentials_to_collection(
            credentials, self._mongo.db.configured_credentials
        )

    def save_stolen_credentials(self, credentials: Sequence[Credentials]):
        MongoCredentialsRepository._save_credentials_to_collection(
            credentials, self._mongo.db.stolen_credentials
        )

    def remove_configured_credentials(self):
        MongoCredentialsRepository._remove_credentials_fom_collection(
            self._mongo.db.configured_credentials
        )

    def remove_stolen_credentials(self):
        MongoCredentialsRepository._remove_credentials_fom_collection(
            self._mongo.db.stolen_credentials
        )

    def remove_all_credentials(self):
        self.remove_configured_credentials()
        self.remove_stolen_credentials()

    @staticmethod
    def _get_credentials_from_collection(collection) -> Sequence[Credentials]:
        try:
            collection_result = []
            list_collection_result = list(collection.find({}))
            for c in list_collection_result:
                del c["_id"]
                collection_result.append(Credentials.from_mapping(c))

            return collection_result
        except Exception as err:
            raise RetrievalError(err)

    @staticmethod
    def _save_credentials_to_collection(credentials: Sequence[Credentials], collection):
        try:
            for c in credentials:
                collection.insert_one(Credentials.to_mapping(c))
        except Exception as err:
            raise StorageError(err)

    @staticmethod
    def _remove_credentials_fom_collection(collection):
        try:
            collection.delete_many({})
        except RemovalError as err:
            raise err
