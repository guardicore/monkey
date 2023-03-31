from pymongo import MongoClient

from monkey_island.cc.models import OTP

from . import IOTPRepository
from .consts import MONGO_OBJECT_ID_KEY
from .errors import RemovalError, RetrievalError, StorageError, UnknownRecordError


class MongoOTPRepository(IOTPRepository):
    def __init__(self, mongo_client: MongoClient):
        self._otp_collection = mongo_client.monkey_island.otp
        self._otp_collection.create_index("otp", unique=True)
        self._otp_collection.create_index("expiration_time", expireAfterSeconds=0)

    def save_otp(self, otp: OTP):
        try:
            # Do we need to encrypt OTPs?
            self._otp_collection.insert_one(otp.dict(simplify=True))
        except Exception as err:
            raise StorageError(f"Error updating otp: {err}")

    def get_otp(self, otp: str) -> OTP:
        try:
            otp_dict = self._otp_collection.find_one({"otp": otp}, {MONGO_OBJECT_ID_KEY: False})
        except Exception as err:
            raise RetrievalError(f"Error retrieving otp: {err}")

        if otp_dict is None:
            raise UnknownRecordError("OTP not found")
        return OTP(**otp_dict)

    def delete_otp(self, otp: str):
        try:
            self._otp_collection.delete_one({"otp": otp})
        except Exception as err:
            raise RemovalError(f"Error deleting otp: {err}")

    def reset(self):
        try:
            self._otp_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the repository: {err}")
