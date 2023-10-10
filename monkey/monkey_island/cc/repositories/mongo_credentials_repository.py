from typing import Any, Dict, Mapping, Sequence

from monkeytypes import Credentials
from pymongo import MongoClient

from monkey_island.cc.repositories import (
    ICredentialsRepository,
    RemovalError,
    RetrievalError,
    StorageError,
)
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from .consts import MONGO_OBJECT_ID_KEY


class MongoCredentialsRepository(ICredentialsRepository):
    """
    Store credentials in a mongo database that can be used to propagate around the network.
    """

    def __init__(self, mongo: MongoClient, repository_encryptor: ILockableEncryptor):
        self._database = mongo.monkey_island
        self._repository_encryptor = repository_encryptor

    def get_configured_credentials(self) -> Sequence[Credentials]:
        return self._get_credentials_from_collection(self._database.configured_credentials)

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        return self._get_credentials_from_collection(self._database.stolen_credentials)

    def get_all_credentials(self) -> Sequence[Credentials]:
        configured_credentials = self.get_configured_credentials()
        stolen_credentials = self.get_stolen_credentials()

        return [*configured_credentials, *stolen_credentials]

    def save_configured_credentials(self, credentials: Sequence[Credentials]):
        # TODO: Fix deduplication of Credentials in mongo
        self._save_credentials_to_collection(credentials, self._database.configured_credentials)

    def save_stolen_credentials(self, credentials: Sequence[Credentials]):
        self._save_credentials_to_collection(credentials, self._database.stolen_credentials)

    def remove_configured_credentials(self):
        self._remove_credentials_fom_collection(self._database.configured_credentials)

    def remove_stolen_credentials(self):
        self._remove_credentials_fom_collection(self._database.stolen_credentials)

    def remove_all_credentials(self):
        self.remove_configured_credentials()
        self.remove_stolen_credentials()

    def reset(self):
        self.remove_all_credentials()

    def _get_credentials_from_collection(self, collection) -> Sequence[Credentials]:
        try:
            collection_result = []
            list_collection_result = list(collection.find({}, {MONGO_OBJECT_ID_KEY: False}))
            for encrypted_credentials in list_collection_result:
                plaintext_credentials = self._decrypt_credentials_mapping(encrypted_credentials)
                collection_result.append(Credentials(**plaintext_credentials))

            return collection_result
        except Exception as err:
            raise RetrievalError(err)

    def _save_credentials_to_collection(self, credentials: Sequence[Credentials], collection):
        try:
            for c in credentials:
                encrypted_credentials = self._encrypt_credentials_mapping(c.dict(simplify=True))
                collection.insert_one(encrypted_credentials)
        except Exception as err:
            raise StorageError(err)

    # TODO: If possible, implement the encryption/decryption as a decorator so it can be reused with
    #       different ICredentialsRepository implementations
    def _encrypt_credentials_mapping(self, mapping: Mapping[str, Any]) -> Mapping[str, Any]:
        encrypted_mapping: Dict[str, Any] = {}

        for secret_or_identity, credentials_component in mapping.items():
            if credentials_component is None:
                encrypted_component = None
            else:
                encrypted_component = {
                    key: self._repository_encryptor.encrypt(value.encode())
                    if value is not None
                    else value
                    for key, value in credentials_component.items()
                }

            encrypted_mapping[secret_or_identity] = encrypted_component

        return encrypted_mapping

    def _decrypt_credentials_mapping(self, mapping: Mapping[str, Any]) -> Mapping[str, Any]:
        decrypted_mapping: Dict[str, Any] = {}

        for secret_or_identity, credentials_component in mapping.items():
            if credentials_component is None:
                decrypted_component = None
            else:
                decrypted_component = {
                    key: self._repository_encryptor.decrypt(value).decode()
                    if value is not None
                    else value
                    for key, value in credentials_component.items()
                }

            decrypted_mapping[secret_or_identity] = decrypted_component

        return decrypted_mapping

    @staticmethod
    def _remove_credentials_fom_collection(collection):
        try:
            collection.drop()
        except Exception as err:
            raise RemovalError(f"Error removing credentials: {err}")
