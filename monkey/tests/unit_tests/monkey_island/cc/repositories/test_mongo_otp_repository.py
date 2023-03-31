from unittest.mock import MagicMock

import mongomock
import pytest

from monkey_island.cc.models import OTP
from monkey_island.cc.repositories import (
    IOTPRepository,
    MongoOTPRepository,
    RemovalError,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

OTPS = (
    OTP(otp="test_otp_1", expiration_time=1),
    OTP(otp="test_otp_2", expiration_time=2),
    OTP(otp="test_otp_3", expiration_time=3),
)


@pytest.fixture
def empty_otp_repository() -> IOTPRepository:
    return MongoOTPRepository(mongomock.MongoClient())


@pytest.fixture
def otp_repository() -> IOTPRepository:
    client = mongomock.MongoClient()
    client.monkey_island.otp.insert_many((o.dict(simplify=True) for o in OTPS))
    otp_repository = MongoOTPRepository(client)
    return otp_repository


@pytest.fixture
def error_raising_mongo_client() -> mongomock.MongoClient:
    client = mongomock.MongoClient()
    client.monkey_island = MagicMock(spec=mongomock.Database)
    client.monkey_island.otp = MagicMock(spec=mongomock.Collection)
    client.monkey_island.otp.insert_one = MagicMock(side_effect=Exception("insert failed"))
    client.monkey_island.otp.find_one = MagicMock(side_effect=Exception("find failed"))
    client.monkey_island.otp.delete_one = MagicMock(side_effect=Exception("delete failed"))
    client.monkey_island.otp.drop = MagicMock(side_effect=Exception("drop failed"))

    return client


@pytest.fixture
def error_raising_otp_repository(error_raising_mongo_client) -> IOTPRepository:
    return MongoOTPRepository(error_raising_mongo_client)


def test_save_otp(empty_otp_repository: IOTPRepository):
    otp = OTP(otp="test_otp", expiration_time=1)
    empty_otp_repository.save_otp(otp)
    assert empty_otp_repository.get_otp("test_otp") == otp


def test_save_otp__prevents_duplicates(otp_repository: IOTPRepository):
    with pytest.raises(StorageError):
        otp_repository.save_otp(OTPS[0])


def test_save_otp__raises_storage_error_if_error_occurs(
    error_raising_otp_repository: IOTPRepository,
):
    with pytest.raises(StorageError):
        error_raising_otp_repository.save_otp(OTP(otp="test_otp", expiration_time=1))


def test_get_otp__raises_unknown_record_error_if_otp_does_not_exist(
    empty_otp_repository: IOTPRepository,
):
    with pytest.raises(UnknownRecordError):
        empty_otp_repository.get_otp("test_otp")


def test_get_otp__returns_otp_if_otp_exists(otp_repository: IOTPRepository):
    assert otp_repository.get_otp(OTPS[0].otp) == OTPS[0]


def test_get_otp__raises_retrieval_error_if_error_occurs(
    error_raising_otp_repository: IOTPRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_otp_repository.get_otp("test_otp")


def test_delete_otp__deletes_otp_if_otp_exists(otp_repository: IOTPRepository):
    otp_repository.delete_otp(OTPS[0].otp)

    with pytest.raises(UnknownRecordError):
        otp_repository.get_otp(OTPS[0].otp)


def test_delete_otp__raises_removal_error_if_error_occurs(
    error_raising_otp_repository: IOTPRepository,
):
    with pytest.raises(RemovalError):
        error_raising_otp_repository.delete_otp("test_otp")


def test_reset__deletes_all_otp(otp_repository: IOTPRepository):
    otp_repository.reset()

    for o in OTPS:
        with pytest.raises(UnknownRecordError):
            otp_repository.get_otp(o.otp)


def test_reset__raises_removal_error_if_error_occurs(error_raising_otp_repository: IOTPRepository):
    with pytest.raises(RemovalError):
        error_raising_otp_repository.reset()
