from unittest.mock import MagicMock

import mongomock
import pytest
from monkeytypes import OperatingSystem

from monkey_island.cc.repositories import RemovalError, RetrievalError, StorageError
from monkey_island.cc.services.agent_binary_service.i_masquerade_repository import (
    IMasqueradeRepository,
)
from monkey_island.cc.services.agent_binary_service.mongo_masquerade_repository import (
    MongoMasqueradeRepository,
)

LINUX_MASQUE = b"linux_m0nk3y"
LINUX_DOCUMENT = {"operating_system": OperatingSystem.LINUX.value, "masque": LINUX_MASQUE}

WINDOWS_MASQUE = b"windows_m0nk3y"
WINDOWS_DOCUMENT = {"operating_system": OperatingSystem.WINDOWS.value, "masque": WINDOWS_MASQUE}


@pytest.fixture
def masquerade_repository() -> IMasqueradeRepository:
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    mongo_client.monkey_island.masques.insert_many([LINUX_DOCUMENT, WINDOWS_DOCUMENT])
    return MongoMasqueradeRepository(mongo_client)


@pytest.fixture
def empty_masquerade_repository() -> IMasqueradeRepository:
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    return MongoMasqueradeRepository(mongo_client)


@pytest.fixture
def error_raising_mock_mongo_client() -> mongomock.MongoClient:
    mongo_client = MagicMock(spec=mongomock.MongoClient)
    mongo_client.monkey_island = MagicMock(spec=mongomock.Database)
    mongo_client.monkey_island.masques = MagicMock(spec=mongomock.Collection)

    mongo_client.monkey_island.masques.drop = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.masques.find = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.masques.find_one = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.masques.replace_one = MagicMock(
        side_effect=Exception("some exception")
    )

    return mongo_client


@pytest.fixture
def error_raising_masquerade_repository(
    error_raising_mock_mongo_client: mongomock.MongoClient,
) -> IMasqueradeRepository:
    return MongoMasqueradeRepository(error_raising_mock_mongo_client)


def test_set_masque__insert(empty_masquerade_repository: IMasqueradeRepository):
    empty_masquerade_repository.set_masque(OperatingSystem.LINUX, LINUX_MASQUE)

    assert empty_masquerade_repository.get_masque(OperatingSystem.LINUX) == LINUX_MASQUE


def test_set_masque__update(masquerade_repository: IMasqueradeRepository):
    new_masque = b"new_windows_m0nk3y"
    masquerade_repository.set_masque(OperatingSystem.WINDOWS, new_masque)

    assert masquerade_repository.get_masque(OperatingSystem.LINUX) == LINUX_MASQUE
    assert masquerade_repository.get_masque(OperatingSystem.WINDOWS) == new_masque


@pytest.mark.parametrize("operating_system", [OperatingSystem.LINUX, OperatingSystem.WINDOWS])
def test_set_masque__clear(
    masquerade_repository: IMasqueradeRepository, operating_system: OperatingSystem
):
    # Ensure the repository is not empty
    masque = masquerade_repository.get_masque(operating_system)
    assert isinstance(masque, bytes)

    masquerade_repository.set_masque(operating_system, None)

    assert masquerade_repository.get_masque(operating_system) is None


def test_set_masque__no_changes(masquerade_repository: IMasqueradeRepository):
    masquerade_repository.set_masque(OperatingSystem.LINUX, LINUX_MASQUE)

    assert masquerade_repository.get_masque(OperatingSystem.LINUX) == LINUX_MASQUE


def test_set_masque__storage_error(error_raising_masquerade_repository: IMasqueradeRepository):
    with pytest.raises(StorageError):
        error_raising_masquerade_repository.set_masque(OperatingSystem.WINDOWS, WINDOWS_MASQUE)


def test_get_masque__empty_repo(empty_masquerade_repository: IMasqueradeRepository):
    masque = empty_masquerade_repository.get_masque(OperatingSystem.LINUX)

    assert masque is None


def test_get_masque(masquerade_repository: IMasqueradeRepository):
    masque = masquerade_repository.get_masque(OperatingSystem.WINDOWS)

    assert masque == WINDOWS_MASQUE


def test_get_masque__empty_masque(masquerade_repository: IMasqueradeRepository):
    empty_bytes = b""

    masquerade_repository.set_masque(OperatingSystem.WINDOWS, empty_bytes)
    masque = masquerade_repository.get_masque(OperatingSystem.WINDOWS)

    assert masque == empty_bytes


def test_get_masque__retrieval_error(error_raising_masquerade_repository: IMasqueradeRepository):
    with pytest.raises(RetrievalError):
        error_raising_masquerade_repository.get_masque(OperatingSystem.LINUX)


def test_reset(masquerade_repository: IMasqueradeRepository):
    # Ensure the repository is not empty
    for operating_system in OperatingSystem:
        masque = masquerade_repository.get_masque(operating_system)
        assert isinstance(masque, bytes)

    masquerade_repository.reset()

    for operating_system in OperatingSystem:
        assert masquerade_repository.get_masque(operating_system) is None


def test_usable_after_reset(masquerade_repository: IMasqueradeRepository):
    masquerade_repository.reset()

    masquerade_repository.set_masque(OperatingSystem.LINUX, LINUX_MASQUE)

    assert masquerade_repository.get_masque(OperatingSystem.LINUX) == LINUX_MASQUE


def test_reset__removal_error(error_raising_masquerade_repository: IMasqueradeRepository):
    with pytest.raises(RemovalError):
        error_raising_masquerade_repository.reset()
