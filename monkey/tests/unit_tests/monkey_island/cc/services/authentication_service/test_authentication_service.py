import time
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
from monkey_island.cc.models import IslandMode
from monkey_island.cc.repositories import UnknownRecordError
from monkey_island.cc.server_utils.encryption import ILockableEncryptor
from monkey_island.cc.services.authentication_service.authentication_facade import (
    OTP_EXPIRATION_TIME,
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.i_otp_repository import IOTPRepository
from monkey_island.cc.services.authentication_service.setup import setup_authentication
from monkey_island.cc.services.authentication_service.token_generator import TokenGenerator
from monkey_island.cc.services.authentication_service.token_parser import (
    TokenParser,
    TokenValidationError,
)
from monkey_island.cc.services.authentication_service.user import User

USERNAME = "user1"
PASSWORD = "test"
PASSWORD_HASH = "$2b$12$yQzymz55fRvm8rApg7erluIvIAKSFSDrNIOIrOlxC4sXsDSkeu9z2"
USERS = [
    User(username="user1", password="test1", fs_uniquifier="a"),
    User(username="user2", password="test2", fs_uniquifier="b"),
    User(username="user3", password="test3", fs_uniquifier="c"),
]


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
def mock_token_generator() -> TokenGenerator:
    return MagicMock(spec=TokenGenerator)


@pytest.fixture
def mock_agent_event_queue() -> IAgentEventQueue:
    return MagicMock(spec=IAgentEventQueue)


@pytest.fixture
def mock_token_parser() -> TokenParser:
    return MagicMock(spec=TokenParser)


@pytest.fixture
def mock_otp_repository() -> IOTPRepository:
    return MagicMock(spec=IOTPRepository)


@pytest.fixture
def authentication_facade(
    mock_flask_app,
    mock_repository_encryptor: ILockableEncryptor,
    mock_island_event_queue: IIslandEventQueue,
    mock_user_datastore: UserDatastore,
    mock_token_generator: TokenGenerator,
    mock_token_parser: TokenParser,
    mock_otp_repository: IOTPRepository,
) -> AuthenticationFacade:
    return AuthenticationFacade(
        mock_repository_encryptor,
        mock_island_event_queue,
        mock_user_datastore,
        mock_token_generator,
        mock_token_parser,
        mock_otp_repository,
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
    assert mock_island_event_queue.publish.call_count == 3
    mock_repository_encryptor.reset_key.assert_called_once()
    mock_repository_encryptor.unlock.assert_called_once()
    mock_island_event_queue.publish.assert_has_calls(
        [
            call(IslandEventTopic.CLEAR_SIMULATION_DATA),
            call(IslandEventTopic.RESET_AGENT_CONFIGURATION),
            call(topic=IslandEventTopic.SET_ISLAND_MODE, mode=IslandMode.UNSET),
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


def test_generate_new_token_pair__generates_tokens(
    mock_token_generator: TokenGenerator,
    mock_token_parser: TokenParser,
    authentication_facade: AuthenticationFacade,
):
    user = User(username=USERNAME, password=PASSWORD, fs_uniquifier="a")
    user.save()
    mock_token_generator.generate_token.return_value = "new_token"
    mock_token_parser.parse.return_value.payload = "a"

    access_token = user.get_auth_token()
    refresh_token = "original_refresh_token"
    new_access_token, new_refresh_token = authentication_facade.generate_new_token_pair(
        refresh_token
    )

    assert access_token != refresh_token
    assert new_access_token != new_refresh_token
    assert new_access_token != access_token
    assert new_refresh_token != refresh_token


def test_generate_new_token_pair__fails_if_user_does_not_exist(
    authentication_facade: AuthenticationFacade,
):
    nonexistent_user = User(username="_", password="_", fs_uniquifier="bogus")
    bogus_token = authentication_facade.generate_refresh_token(nonexistent_user)
    authentication_facade._datastore.find_user = MagicMock(return_value=None)

    with pytest.raises(Exception):
        authentication_facade.generate_new_token_pair(bogus_token)


def test_generate_new_token_pair__fails_if_token_invalid(
    mock_token_parser: TokenParser,
    authentication_facade: AuthenticationFacade,
):
    user = User(username=USERNAME, password=PASSWORD, fs_uniquifier="a")
    user.save()
    refresh_token = authentication_facade.generate_refresh_token(user)
    mock_token_parser.parse.side_effect = TokenValidationError()

    with pytest.raises(TokenValidationError):
        authentication_facade.generate_new_token_pair(refresh_token)


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


def test_generate_otp__uses_expected_expiration_time(
    freezer, authentication_facade: AuthenticationFacade, mock_otp_repository: IOTPRepository
):
    authentication_facade.generate_otp()

    expiration_time = mock_otp_repository.insert_otp.call_args[0][1]
    expected_expiration_time = time.monotonic() + OTP_EXPIRATION_TIME
    assert expiration_time == expected_expiration_time


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
