from pathlib import Path
from unittest.mock import MagicMock, call

import mongomock
import pymongo
import pytest
from flask_security import UserDatastore
from tests.common import StubDIContainer

from common.event_queue import IAgentEventQueue
from common.types import OTP
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic
from monkey_island.cc.repositories import UnknownRecordError
from monkey_island.cc.server_utils.encryption import ILockableEncryptor
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.i_otp_repository import IOTPRepository
from monkey_island.cc.services.authentication_service.mongo_otp_repository import MongoOTPRepository
from monkey_island.cc.services.authentication_service.setup import setup_authentication
from monkey_island.cc.services.authentication_service.user import User

USERNAME = "user1"
PASSWORD = "test"
PASSWORD_HASH = "$2b$12$yQzymz55fRvm8rApg7erluIvIAKSFSDrNIOIrOlxC4sXsDSkeu9z2"
USERS = [
    User(username="user1", password="test1", fs_uniquifier="a"),
    User(username="user2", password="test2", fs_uniquifier="b"),
    User(username="user3", password="test3", fs_uniquifier="c"),
]

TOKEN_TTL_SEC = 10

# Some tests have these fixtures as arguments even though `autouse=True`, because
# to access the object that a fixture returns, it needs to be specified as an argument.
# See https://stackoverflow.com/a/37046403.


@pytest.fixture
def mock_repository_encryptor() -> ILockableEncryptor:
    return MagicMock(spec=ILockableEncryptor)


@pytest.fixture
def mock_island_event_queue() -> IIslandEventQueue:
    return MagicMock(spec=IIslandEventQueue)


@pytest.fixture
def mock_user_datastore() -> UserDatastore:
    return MagicMock(spec=UserDatastore)


@pytest.fixture
def mock_agent_event_queue() -> IAgentEventQueue:
    return MagicMock(spec=IAgentEventQueue)


@pytest.fixture
def mock_otp_repository() -> IOTPRepository:
    return MagicMock(spec=IOTPRepository)


@pytest.fixture
def authentication_facade(
    mock_flask_app,
    mock_repository_encryptor: ILockableEncryptor,
    mock_island_event_queue: IIslandEventQueue,
    mock_user_datastore: UserDatastore,
    mock_otp_repository: IOTPRepository,
) -> AuthenticationFacade:
    return AuthenticationFacade(
        mock_repository_encryptor,
        mock_island_event_queue,
        mock_user_datastore,
        mock_otp_repository,
        TOKEN_TTL_SEC,
    )


def test_needs_registration__true(authentication_facade: AuthenticationFacade):
    authentication_facade._datastore.find_user.return_value = False
    assert authentication_facade.needs_registration()


def test_needs_registration__false(
    monkeypatch,
    authentication_facade: AuthenticationFacade,
):
    authentication_facade._datastore.find_user.return_value = True
    assert not authentication_facade.needs_registration()


def test_handle_successful_registration(
    mock_repository_encryptor: ILockableEncryptor,
    mock_island_event_queue: IIslandEventQueue,
    authentication_facade: AuthenticationFacade,
):
    authentication_facade.handle_successful_registration(USERNAME, PASSWORD)

    assert mock_repository_encryptor.unlock.call_args[0][0] != USERNAME
    assert mock_repository_encryptor.unlock.call_args[0][0] != PASSWORD
    assert mock_island_event_queue.publish.call_count == 2
    mock_repository_encryptor.reset_key.assert_called_once()
    mock_repository_encryptor.unlock.assert_called_once()
    mock_island_event_queue.publish.assert_has_calls(
        [
            call(IslandEventTopic.CLEAR_SIMULATION_DATA),
            call(IslandEventTopic.RESET_AGENT_CONFIGURATION),
        ]
    )


def test_handle_sucessful_login(
    mock_repository_encryptor: ILockableEncryptor,
    authentication_facade: AuthenticationFacade,
):
    authentication_facade.handle_successful_login(USERNAME, PASSWORD)

    mock_repository_encryptor.unlock.assert_called_once()
    assert mock_repository_encryptor.unlock.call_args[0][0] != USERNAME
    assert mock_repository_encryptor.unlock.call_args[0][0] != PASSWORD


def test_refresh_user_token(
    mock_user_datastore: UserDatastore, authentication_facade: AuthenticationFacade
):
    def reset_uniquifier(user: User):
        user.fs_uniquifier = "b"

    mock_user_datastore.set_uniquifier.side_effect = reset_uniquifier
    user = User(username=USERNAME, password=PASSWORD, fs_uniquifier="a")

    original_access_token = str(user.get_auth_token())
    new_access_token, token_ttl_sec = authentication_facade.refresh_user_token(user)

    mock_user_datastore.set_uniquifier.assert_called_once()
    assert mock_user_datastore.set_uniquifier.call_args[0][0].username == user.username
    assert new_access_token.get_secret_value() != original_access_token
    assert token_ttl_sec == TOKEN_TTL_SEC


def test_remove_user__removes_user(
    mock_user_datastore: UserDatastore, authentication_facade: AuthenticationFacade
):
    user = User(username=USERNAME, password=PASSWORD, fs_uniquifier="a")
    mock_user_datastore.find_user.return_value = user

    authentication_facade.remove_user(user.username)

    mock_user_datastore.delete_user.assert_called_once_with(user)


def test_remove_user__is_idempotent(
    mock_user_datastore: UserDatastore, authentication_facade: AuthenticationFacade
):
    mock_user_datastore.find_user = MagicMock(return_value=None)

    authentication_facade.remove_user(USERNAME)


def test_revoke_all_tokens_for_all_users(
    mock_user_datastore: UserDatastore,
    authentication_facade: AuthenticationFacade,
):
    for user in USERS:
        user.save(force_insert=True)
    authentication_facade.revoke_all_tokens_for_all_users()

    assert mock_user_datastore.set_uniquifier.call_count == len(USERS)
    for user in USERS:
        mock_user_datastore.set_uniquifier.assert_any_call(user)


def test_generate_otp__saves_otp(
    authentication_facade: AuthenticationFacade, mock_otp_repository: IOTPRepository
):
    otp = authentication_facade.generate_otp()

    assert mock_otp_repository.insert_otp.call_args[0][0] == otp


TIME = "2020-01-01 00:00:00"
TIME_FLOAT = 1577836800.0


@pytest.mark.parametrize(
    "otp_is_used_return_value, get_expiration_return_value, otp_is_valid_expected_value",
    [
        (False, TIME_FLOAT - 1, False),  # not used, after expiration time
        (True, TIME_FLOAT - 1, False),  # used, after expiration time
        (False, TIME_FLOAT, True),  # not used, at expiration time
        (True, TIME_FLOAT, False),  # used, at expiration time
        (False, TIME_FLOAT + 1, True),  # not used, before expiration time
        (True, TIME_FLOAT + 1, False),  # used, before expiration time
    ],
)
def test_authorize_otp(
    authentication_facade: AuthenticationFacade,
    mock_otp_repository: IOTPRepository,
    freezer,
    otp_is_used_return_value: bool,
    get_expiration_return_value: int,
    otp_is_valid_expected_value: bool,
):
    otp = OTP("secret")

    freezer.move_to(TIME)

    mock_otp_repository.otp_is_used.return_value = otp_is_used_return_value
    mock_otp_repository.get_expiration.return_value = get_expiration_return_value

    assert authentication_facade.authorize_otp(otp) == otp_is_valid_expected_value
    mock_otp_repository.set_used.assert_called_once()


def test_authorize_otp__unknown_otp(
    authentication_facade: AuthenticationFacade,
    mock_otp_repository: IOTPRepository,
):
    otp = OTP("secret")

    mock_otp_repository.otp_is_used.side_effect = UnknownRecordError(f"Unknown otp {otp}")
    mock_otp_repository.set_used.side_effect = UnknownRecordError(f"Unknown otp {otp}")
    mock_otp_repository.get_expiration.side_effect = UnknownRecordError(f"Unknown otp {otp}")

    assert authentication_facade.authorize_otp(otp) is False


# mongomock.MongoClient is not a pymongo.MongoClient. This class allows us to register a
# mongomock.MongoClient as a pymongo.MongoClient with the StubDIContainer.
class MockMongoClient(mongomock.MongoClient, pymongo.MongoClient):
    pass


def test_setup_authentication__revokes_tokens(
    monkeypatch,
    mock_flask_app,
    mock_user_datastore: UserDatastore,
    mock_island_event_queue: IIslandEventQueue,
    mock_repository_encryptor: ILockableEncryptor,
    mock_agent_event_queue: IAgentEventQueue,
):
    for user in USERS:
        user.save(force_insert=True)

    mock_security = MagicMock(datastore=mock_user_datastore)
    monkeypatch.setattr(
        "monkey_island.cc.services.authentication_service.setup.configure_flask_security",
        lambda *args: mock_security,
    )

    container = StubDIContainer()
    container.register_instance(ILockableEncryptor, mock_repository_encryptor)
    container.register_instance(IIslandEventQueue, mock_island_event_queue)
    container.register_instance(IAgentEventQueue, mock_agent_event_queue)
    container.register_instance(pymongo.MongoClient, MockMongoClient())
    setup_authentication(MagicMock(), MagicMock(), container, Path("data_dir"), MagicMock())

    assert mock_user_datastore.set_uniquifier.call_count == len(USERS)
    for user in USERS:
        mock_user_datastore.set_uniquifier.assert_any_call(user)


def test_setup_authentication__invalidates_otps(
    monkeypatch,
    mock_flask_app,
    mock_agent_event_queue: IAgentEventQueue,
    mock_island_event_queue: IIslandEventQueue,
    mock_repository_encryptor: ILockableEncryptor,
):
    mock_otp_repository = MagicMock(spec=MongoOTPRepository)
    mock_security = MagicMock()
    mock_security.datastore = mock_user_datastore
    monkeypatch.setattr(
        "monkey_island.cc.services.authentication_service.setup.configure_flask_security",
        lambda *args: mock_security,
    )

    container = StubDIContainer()
    container.register_instance(MongoOTPRepository, mock_otp_repository)
    container.register_instance(ILockableEncryptor, mock_repository_encryptor)
    container.register_instance(IIslandEventQueue, mock_island_event_queue)
    container.register_instance(IAgentEventQueue, mock_agent_event_queue)
    container.register_instance(pymongo.MongoClient, MockMongoClient())

    setup_authentication(MagicMock(), MagicMock(), container, Path("data_dir"), MagicMock())

    assert mock_otp_repository.reset.called
