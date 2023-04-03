from pymongo import MongoClient

from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from . import IOTPRepository
from .consts import MONGO_OBJECT_ID_KEY
from .errors import RemovalError, RetrievalError, StorageError, UnknownRecordError


class MongoOTPRepository(IOTPRepository):
    def __init__(
        self,
        mongo_client: MongoClient,
        encryptor: ILockableEncryptor,
    ):
        self._encryptor = encryptor
        self._otp_collection = mongo_client.monkey_island.otp
        self._otp_collection.create_index("otp", unique=True)

    def insert_otp(self, otp: str, expiration: float):
        try:
            encrypted_otp = self._encryptor.encrypt(otp.encode())
            self._otp_collection.insert_one({"otp": encrypted_otp, "expiration_time": expiration})
        except Exception as err:
            raise StorageError(f"Error updating otp: {err}")

    def get_expiration(self, otp: str) -> float:
        try:
            encrypted_otp = self._encryptor.encrypt(otp.encode())
            otp_dict = self._otp_collection.find_one(
                {"otp": encrypted_otp}, {MONGO_OBJECT_ID_KEY: False}
            )
        except Exception as err:
            raise RetrievalError(f"Error retrieving otp: {err}")

        if otp_dict is None:
            raise UnknownRecordError("OTP not found")
        return otp_dict["expiration_time"]

    def reset(self):
        try:
            self._otp_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the repository: {err}")
