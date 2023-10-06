import hashlib
import secrets
from functools import lru_cache
from typing import Any, Mapping

from bson.objectid import ObjectId
from monkeytypes import OTP
from pymongo import MongoClient

from monkey_island.cc.repositories import (
    MONGO_OBJECT_ID_KEY,
    RemovalError,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

from .i_otp_repository import IOTPRepository


class MongoOTPRepository(IOTPRepository):
    def __init__(
        self,
        mongo_client: MongoClient,
    ):
        # SECURITY: A new salt is generated for each instance of this repository. This effectively
        # makes all preexisting OTPS invalid on Island startup.
        self._salt = secrets.token_bytes(16)

        self._otp_collection = mongo_client.monkey_island.otp
        self._otp_collection.create_index("otp", unique=True)

    def insert_otp(self, otp: OTP, expiration: float):
        try:
            self._otp_collection.insert_one(
                {"otp": self._hash_otp(otp), "expiration_time": expiration, "used": False}
            )
        except Exception as err:
            raise StorageError(f"Error inserting OTP: {err}")

    def _hash_otp(self, otp: OTP) -> bytes:
        # SECURITY: A single round of salted SHA256 is usually not considered sufficient for
        # protecting passwords. However, OTPs have a very short life span (2 minutes at the time of
        # this writing). Additionally, they can only be used once. Finally, they are 32 bytes long.
        # At the present time, we consider this to be sufficient protection. I'm unaware of any
        # technology in existence that can brute force SHA256 for (roughly) 48-byte inputs in under
        # 2 minutes.
        #
        # Note that if any of these conditions change (timeouts become very long or OTPs become very
        # short), this should be revisited. For now, we prefer the significantly faster performance
        # of a single round of salted SHA256 over a more secure but slower algorithm.
        otp_bytes = otp.get_secret_value().encode()
        return hashlib.sha256(self._salt + otp_bytes).digest()

    def set_used(self, otp: OTP):
        try:
            otp_id = self._get_otp_object_id(otp)
            self._otp_collection.update_one({MONGO_OBJECT_ID_KEY: otp_id}, {"$set": {"used": True}})
        except UnknownRecordError as err:
            raise err
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
        retrieval_error_message = f"Error retrieving OTP with ID {otp_object_id}"

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
            otp_dict = self._otp_collection.find_one(
                {"otp": self._hash_otp(otp)}, [MONGO_OBJECT_ID_KEY]
            )
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
