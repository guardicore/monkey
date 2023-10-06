from dataclasses import dataclass
from unittest.mock import MagicMock

import mongomock
import pytest
from monkeytypes import OTP

from monkey_island.cc.repositories import (
    RemovalError,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)
from monkey_island.cc.services.authentication_service.i_otp_repository import IOTPRepository
from monkey_island.cc.services.authentication_service.mongo_otp_repository import MongoOTPRepository


@dataclass
class OTPData:
    otp: str
    expiration_time: float


OTPS = (
    OTPData(otp=OTP("test_otp_1"), expiration_time=1),
    OTPData(otp=OTP("test_otp_2"), expiration_time=2),
    OTPData(otp=OTP("test_otp_3"), expiration_time=3),
)


@pytest.fixture
def mongo_client() -> mongomock.MongoClient:
    return mongomock.MongoClient()


@pytest.fixture
def otp_repository(mongo_client: mongomock.MongoClient) -> IOTPRepository:
    return MongoOTPRepository(mongo_client)


@pytest.fixture
def error_raising_mongo_client() -> mongomock.MongoClient:
    client = mongomock.MongoClient()
    client.monkey_island = MagicMock(spec=mongomock.Database)
    client.monkey_island.otp = MagicMock(spec=mongomock.Collection)
    client.monkey_island.otp.insert_one = MagicMock(side_effect=Exception("insert failed"))
    client.monkey_island.otp.update_one = MagicMock(side_effect=Exception("insert failed"))
    client.monkey_island.otp.find_one = MagicMock(side_effect=Exception("find failed"))
    client.monkey_island.otp.delete_one = MagicMock(side_effect=Exception("delete failed"))
    client.monkey_island.otp.drop = MagicMock(side_effect=Exception("drop failed"))

    return client


@pytest.fixture
def error_raising_otp_repository(
    error_raising_mongo_client, repository_encryptor
) -> IOTPRepository:
    return MongoOTPRepository(error_raising_mongo_client)


def test_insert_otp(otp_repository: IOTPRepository):
    otp_repository.insert_otp(OTPS[1].otp, 1)
    assert otp_repository.get_expiration(OTPS[1].otp) == 1


def test_insert_otp__prevents_duplicates(otp_repository: IOTPRepository):
    otp_repository.insert_otp(OTPS[0].otp, OTPS[0].expiration_time)
    with pytest.raises(StorageError):
        otp_repository.insert_otp(OTPS[0].otp, OTPS[0].expiration_time)


def test_insert_otp__prevents_duplicate_otp_with_differing_expiration(
    otp_repository: IOTPRepository,
):
    otp_repository.insert_otp(OTPS[0].otp, 11)
    with pytest.raises(StorageError):
        otp_repository.insert_otp(OTPS[0].otp, 99)


def test_insert_otp__raises_storage_error_if_error_occurs(
    error_raising_otp_repository: IOTPRepository,
):
    with pytest.raises(StorageError):
        error_raising_otp_repository.insert_otp("test_otp", 1)


def test_get_expiration__raises_unknown_record_error_if_otp_does_not_exist(
    otp_repository: IOTPRepository,
):
    with pytest.raises(UnknownRecordError):
        otp_repository.get_expiration(OTPS[2].otp)


@pytest.mark.parametrize("OTP", OTPS)
def test_get_expiration__returns_expiration_if_otp_exists(
    OTP: OTPData, otp_repository: IOTPRepository
):
    otp_repository.insert_otp(OTP.otp, OTP.expiration_time)
    assert otp_repository.get_expiration(OTP.otp) == OTP.expiration_time


def test_get_expiration__raises_retrieval_error_if_error_occurs(
    error_raising_otp_repository: IOTPRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_otp_repository.get_expiration(OTPS[0].otp)


def test_reset__deletes_all_otp(otp_repository: IOTPRepository):
    for o in OTPS:
        otp_repository.insert_otp(o.otp, o.expiration_time)

    otp_repository.reset()

    for o in OTPS:
        with pytest.raises(UnknownRecordError):
            otp_repository.get_expiration(o.otp)


def test_reset__raises_removal_error_if_error_occurs(error_raising_otp_repository: IOTPRepository):
    with pytest.raises(RemovalError):
        error_raising_otp_repository.reset()


def test_set_used(otp_repository: IOTPRepository):
    otp = OTP("test_otp")
    otp_repository.insert_otp(otp, 1)
    assert not otp_repository.otp_is_used(otp)

    otp_repository.set_used(otp)
    assert otp_repository.otp_is_used(otp)


def test_set_used__storage_error(
    error_raising_mongo_client: mongomock.MongoClient, error_raising_otp_repository: IOTPRepository
):
    error_raising_mongo_client.monkey_island.otp.find_one.side_effect = None
    with pytest.raises(StorageError):
        error_raising_otp_repository.set_used(OTP("test_otp"))


def test_set_used__unknown_record_error(otp_repository: IOTPRepository):
    with pytest.raises(UnknownRecordError):
        otp_repository.set_used(OTP("test_otp"))


def test_set_used__idempotent(otp_repository: IOTPRepository):
    otp = OTP("test_otp")
    otp_repository.insert_otp(otp, 1)

    otp_repository.set_used(otp)
    otp_repository.set_used(otp)
    otp_repository.set_used(otp)

    assert otp_repository.otp_is_used(otp)
