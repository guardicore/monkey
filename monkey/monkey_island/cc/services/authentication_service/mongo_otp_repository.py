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

    def update_otp(self, otp: OTP, **kwargs):
        try:
            encrypted_otp = self._encryptor.encrypt(otp.encode())
            self._otp_collection.update_one({"otp": encrypted_otp}, {"$set": kwargs})
        except Exception as err:
            raise StorageError(f"Error updating OTP: {err}")

    def get_expiration(self, otp: OTP) -> float:
        try:
            encrypted_otp = self._encryptor.encrypt(otp.encode())
            otp_dict = self._otp_collection.find_one(
                {"otp": encrypted_otp}, {MONGO_OBJECT_ID_KEY: False}
            )
        except Exception as err:
            raise RetrievalError(f"Error retrieving OTP: {err}")

        if otp_dict is None:
            raise UnknownRecordError("OTP not found")
        return otp_dict["expiration_time"]

    def otp_is_used(self, otp: OTP) -> bool:
        try:
            encrypted_otp = self._encryptor.encrypt(otp.encode())
            otp_dict = self._otp_collection.find_one(
                {"otp": encrypted_otp}, {MONGO_OBJECT_ID_KEY: False}
            )
        except Exception as err:
            raise RetrievalError(f"Error retrieving OTP: {err}")

        if otp_dict is None:
            raise UnknownRecordError("OTP not found")

        return otp_dict["used"]

    def reset(self):
        try:
            self._otp_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the OTP repository: {err}")
