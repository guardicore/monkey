from typing import Sequence

from common.credentials import Credentials
from monkey_island.cc.database import mongo
from monkey_island.cc.repository import RemovalError, RetrievalError, StorageError
from monkey_island.cc.repository.i_credentials_repository import ICredentialsRepository


class MongoCredentialsRepository(ICredentialsRepository):
    """
    Store credentials in a mongo database that can be used to propagate around the network.
    """

    def get_configured_credentials(self) -> Sequence[Credentials]:
        try:
            configured_credentials = list(mongo.db.configured_credentials.find({}))
            return configured_credentials
        except Exception as err:
            raise RetrievalError(err)

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        try:
            stolen_credentials = list(mongo.db.stolen_credentials.find({}))
            return stolen_credentials
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
        try:
            mongo.db.configured_credentials.insert_many(credentials)
        except Exception as err:
            raise StorageError(err)

    def save_stolen_credentials(self, credentials: Sequence[Credentials]):
        try:
            mongo.db.stolen_credentials.insert_many(credentials)
        except Exception as err:
            raise StorageError(err)

    def remove_configured_credentials(self):
        try:
            mongo.db.configured_credentials.remove({})
        except Exception as err:
            raise RemovalError(err)

    def remove_stolen_credentials(self):
        try:
            mongo.db.stolen_credentials.remove({})
        except Exception as err:
            raise RemovalError(err)

    def remove_all_credentials(self):
        try:
            self.remove_configured_credentials()
            self.remove_stolen_credentials()
        except RemovalError as err:
            raise err
