from typing import Sequence

from flask_pymongo import PyMongo

from common.credentials import Credentials
from monkey_island.cc.repository import RemovalError, RetrievalError, StorageError
from monkey_island.cc.repository.i_credentials_repository import ICredentialsRepository


class MongoCredentialsRepository(ICredentialsRepository):
    """
    Store credentials in a mongo database that can be used to propagate around the network.
    """

    def __init__(self, mongo_db: PyMongo):
        self._mongo = mongo_db

    def get_configured_credentials(self) -> Sequence[Credentials]:
        try:

            return MongoCredentialsRepository._get_credentials_from_collection(
                self._mongo.db.configured_credentials
            )
        except Exception as err:
            raise RetrievalError(err)

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        try:
            return MongoCredentialsRepository._get_credentials_from_collection(
                self._mongo.db.stolen_credentials
            )
        except Exception as err:
            raise RetrievalError(err)

    def get_all_credentials(self) -> Sequence[Credentials]:
        try:
            configured_credentials = self.get_configured_credentials()
            stolen_credentials = self.get_stolen_credentials()

            return [*configured_credentials, *stolen_credentials]
        except RetrievalError as err:
            raise err

    def save_configured_credentials(self, credentials: Sequence[Credentials]):
        # TODO: Fix deduplication of Credentials in mongo
        try:
            MongoCredentialsRepository._save_credentials_to_collection(
                credentials, self._mongo.db.configured_credentials
            )
        except Exception as err:
            raise StorageError(err)

    def save_stolen_credentials(self, credentials: Sequence[Credentials]):
        # TODO: Fix deduplication of Credentials in mongo
        try:
            MongoCredentialsRepository._save_credentials_to_collection(
                credentials, self._mongo.db.stolen_credentials
            )
        except Exception as err:
            raise StorageError(err)

    def remove_configured_credentials(self):
        try:
            MongoCredentialsRepository._delete_collection(self._mongo.db.configured_credentials)
        except Exception as err:
            raise RemovalError(err)

    def remove_stolen_credentials(self):
        try:
            MongoCredentialsRepository._delete_collection(self._mongo.db.stolen_credentials)
        except Exception as err:
            raise RemovalError(err)

    def remove_all_credentials(self):
        try:
            self.remove_configured_credentials()
            self.remove_stolen_credentials()
        except RemovalError as err:
            raise err

    @staticmethod
    def _get_credentials_from_collection(collection) -> Sequence[Credentials]:
        collection_result = []
        list_collection_result = list(collection.find({}))
        for c in list_collection_result:
            del c["_id"]
            collection_result.append(Credentials.from_mapping(c))

        return collection_result

    @staticmethod
    def _save_credentials_to_collection(credentials: Sequence[Credentials], collection):
        for c in credentials:
            collection.insert_one(Credentials.to_mapping(c))

    @staticmethod
    def _delete_collection(collection):
        collection.delete_many({})
