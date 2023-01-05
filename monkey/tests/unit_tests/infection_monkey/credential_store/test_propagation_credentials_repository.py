from multiprocessing import Queue, get_context
from time import sleep
from typing import Sequence

import pytest
from pydantic import SecretStr
from tests.data_for_tests.propagation_credentials import (
    CREDENTIALS,
    PASSWORD_1,
    PASSWORD_3,
    USERNAME,
)

from common.agent_configuration import AgentConfiguration
from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username
from infection_monkey.i_control_channel import IControlChannel
from infection_monkey.propagation_credentials_repository import PropagationCredentialsRepository
from infection_monkey.propagation_credentials_repository.propagation_credentials_repository import (
    CREDENTIALS_POLL_PERIOD_SEC,
)

STOLEN_USERNAME_1 = "user1"
STOLEN_USERNAME_2 = "user2"
STOLEN_USERNAME_3 = "user3"
STOLEN_PASSWORD_1 = SecretStr("abcdefg")
STOLEN_PASSWORD_2 = SecretStr("super_secret")
STOLEN_PUBLIC_KEY_1 = "some_public_key_1"
STOLEN_PUBLIC_KEY_2 = "some_public_key_2"
STOLEN_LM_HASH = SecretStr("AAD3B435B51404EEAAD3B435B51404EE")
STOLEN_NT_HASH = SecretStr("C0172DFF622FE29B5327CB79DC12D24C")
STOLEN_PRIVATE_KEY_1 = SecretStr("some_private_key_1")
STOLEN_PRIVATE_KEY_2 = SecretStr("some_private_key_2")
STOLEN_CREDENTIALS = [
    Credentials(
        identity=Username(username=STOLEN_USERNAME_1),
        secret=Password(password=PASSWORD_1),
    ),
    Credentials(
        identity=Username(username=STOLEN_USERNAME_1), secret=Password(password=STOLEN_PASSWORD_1)
    ),
    Credentials(
        identity=Username(username=STOLEN_USERNAME_2),
        secret=SSHKeypair(public_key=STOLEN_PUBLIC_KEY_1, private_key=STOLEN_PRIVATE_KEY_1),
    ),
    Credentials(
        identity=None,
        secret=Password(password=STOLEN_PASSWORD_2),
    ),
    Credentials(
        identity=Username(username=STOLEN_USERNAME_2), secret=LMHash(lm_hash=STOLEN_LM_HASH)
    ),
    Credentials(
        identity=Username(username=STOLEN_USERNAME_2), secret=NTHash(nt_hash=STOLEN_NT_HASH)
    ),
    Credentials(identity=Username(username=STOLEN_USERNAME_3), secret=None),
]

STOLEN_SSH_KEYS_CREDENTIALS = [
    Credentials(
        identity=Username(username=USERNAME),
        secret=SSHKeypair(public_key=STOLEN_PUBLIC_KEY_2, private_key=STOLEN_PRIVATE_KEY_2),
    )
]

NEW_CREDENTIALS = [
    Credentials(
        identity=Username(username="new"),
        secret=Password(password=PASSWORD_3),
    )
]


class BaseControlChannel(IControlChannel):
    def should_agent_stop(self) -> bool:
        pass

    def get_config(self) -> AgentConfiguration:
        pass

    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        pass


@pytest.fixture
def control_channel() -> IControlChannel:
    return StubControlChannel(CREDENTIALS)


class StubControlChannel(BaseControlChannel):
    def __init__(self, credentials: Sequence[Credentials]):
        self._credentials = credentials

        self._calls = get_context("spawn").Value("i", 0)

    @property
    def calls(self):
        return self._calls.value

    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        with self._calls.get_lock():
            self._calls.value += 1
            return self._credentials


@pytest.fixture
def propagation_credentials_repository(
    control_channel: StubControlChannel,
) -> PropagationCredentialsRepository:
    return PropagationCredentialsRepository(control_channel)


def test_get_credentials__retrieves_from_control_channel(propagation_credentials_repository):
    actual_stored_credentials = propagation_credentials_repository.get_credentials()

    assert set(actual_stored_credentials) == set(CREDENTIALS)


def test_add_credentials(propagation_credentials_repository):
    propagation_credentials_repository.add_credentials(STOLEN_CREDENTIALS)
    propagation_credentials_repository.add_credentials(STOLEN_SSH_KEYS_CREDENTIALS)

    actual_stored_credentials = propagation_credentials_repository.get_credentials()

    assert set(actual_stored_credentials) == set(
        STOLEN_CREDENTIALS + STOLEN_SSH_KEYS_CREDENTIALS + CREDENTIALS
    )


def test_credentials_obtained_if_propagation_credentials_fails(
    propagation_credentials_repository: PropagationCredentialsRepository,
    control_channel: StubControlChannel,
    monkeypatch,
):
    def func() -> Sequence[Credentials]:
        raise Exception("No credentials for you!")

    monkeypatch.setattr(control_channel, "get_credentials_for_propagation", func)

    credentials = propagation_credentials_repository.get_credentials()

    assert credentials is not None


def test_get_credentials__uses_cached_credentials(
    propagation_credentials_repository: PropagationCredentialsRepository,
    control_channel: StubControlChannel,
):
    credentials1 = propagation_credentials_repository.get_credentials()
    credentials2 = propagation_credentials_repository.get_credentials()

    assert set(credentials1) == set(credentials2)
    assert control_channel.calls == 1


def get_credentials(
    propagation_credentials_repository: PropagationCredentialsRepository, queue: Queue
):
    credentials = propagation_credentials_repository.get_credentials()
    queue.put(credentials)


def test_get_credentials__used_cached_credentials_multiprocess(
    propagation_credentials_repository: PropagationCredentialsRepository,
    control_channel: StubControlChannel,
):
    context = get_context("spawn")
    queue = context.Queue()
    p1 = context.Process(target=get_credentials, args=(propagation_credentials_repository, queue))
    p2 = context.Process(target=get_credentials, args=(propagation_credentials_repository, queue))
    p1.start()
    p2.start()
    credentials1 = queue.get()
    credentials2 = queue.get()
    p1.join()
    p2.join()

    assert set(credentials1) == set(credentials2)
    assert control_channel.calls == 1


@pytest.mark.skip
@pytest.mark.slow
def test_get_credentials__updates_cache_after_timeout_period(
    propagation_credentials_repository: PropagationCredentialsRepository,
    control_channel: StubControlChannel,
):
    context = get_context("spawn")
    queue = context.Queue()
    p1 = context.Process(target=get_credentials, args=(propagation_credentials_repository, queue))
    p1.start()
    p1.join()

    # Sleep so that the poll period times out
    sleep(CREDENTIALS_POLL_PERIOD_SEC + 0.01)

    p2 = context.Process(target=get_credentials, args=(propagation_credentials_repository, queue))
    p2.start()
    p2.join()

    assert control_channel.calls == 2
