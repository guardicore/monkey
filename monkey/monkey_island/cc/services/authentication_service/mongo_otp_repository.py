from functools import lru_cache
from typing import Any, Mapping

from bson.objectid import ObjectId
from pymongo import MongoClient

from monkey_island.cc.repositories import (
    MONGO_OBJECT_ID_KEY,
    RemovalError,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from .i_otp_repository import IOTPRepository
from .types import OTP


class MongoOTPRepository(IOTPRepository):
    def __init__(
        self,
        mongo_client: MongoClient,
        encryptor: ILockableEncryptor,
    ):
        self._encryptor = encryptor
        self._otp_collection = mongo_client.monkey_island.otp
        self._otp_collection.create_index("otp", unique=True)

    def insert_otp(self, otp: OTP, expiration: float):
        try:
            encrypted_otp = self._encryptor.encrypt(otp.encode())
            self._otp_collection.insert_one(
                {"otp": encrypted_otp, "expiration_time": expiration, "used": False}
            )
        except Exception as err:
            raise StorageError(f"Error inserting OTP: {err}")

    def set_used(self, otp: OTP):
        otp_id = self._get_otp_object_id(otp)

        try:
            self._otp_collection.update_one({MONGO_OBJECT_ID_KEY: otp_id}, {"$set": {"used": True}})
        except Exception as err:
            raise StorageError(f"Error updating OTP: {err}")

    def get_expiration(self, otp: OTP) -> float:
        otp_dict = self._get_otp_document(otp)
        return otp_dict["expiration_time"]

    def otp_is_used(self, otp: OTP) -> bool:
        otp_dict = self._get_otp_document(otp)
        return otp_dict["used"]

    def _get_otp_document(self, otp: OTP) -> Mapping[str, Any]:
        otp_object_id = self._get_otp_object_id(otp)
        retrieval_error_message = f"Error retrieving OTP {otp} with ID {otp_object_id}"

        try:
            otp_dict = self._otp_collection.find_one(
                {"_id": otp_object_id}, {MONGO_OBJECT_ID_KEY: False}
            )
        except Exception as err:
            raise RetrievalError(f"{retrieval_error_message}: {err}")

        if otp_dict is None:
            raise RetrievalError(retrieval_error_message)

        return otp_dict

    @lru_cache
    def _get_otp_object_id(self, otp: OTP) -> ObjectId:
        try:
            encrypted_otp = self._encryptor.encrypt(otp.encode())
            otp_dict = self._otp_collection.find_one({"otp": encrypted_otp}, [MONGO_OBJECT_ID_KEY])
        except Exception as err:
            raise RetrievalError(f"Error retrieving OTP: {err}")

        if otp_dict is None:
            raise UnknownRecordError("OTP not found")

        return otp_dict[MONGO_OBJECT_ID_KEY]

    def reset(self):
        try:
            self._otp_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the OTP repository: {err}")
