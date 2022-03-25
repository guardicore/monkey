from unittest.mock import MagicMock

import pytest

from infection_monkey.credential_store import AggregatingCredentialsStore

DEFAULT_CREDENTIALS = {
    "exploit_user_list": ["Administrator", "root", "user1"],
    "exploit_password_list": [
        "root",
        "123456",
        "password",
        "123456789",
    ],
    "exploit_lm_hash_list": ["aasdf23asd1fdaasadasdfas"],
    "exploit_ntlm_hash_list": ["qw4trklxklvznksbhasd1231", "asdfadvxvsdftw3e3421234123412"],
    "exploit_ssh_keys": [
        {
            "public_key": "ssh-ed25519 AAAAC3NzEIFaJ7xH+Yoxd\n",
            "private_key": "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BdHIAAAAGYXjl0j66VAKruPEKjS3A=\n"
            "-----END OPENSSH PRIVATE KEY-----\n",
            "user": "ubuntu",
            "ip": "10.0.3.15",
        },
        {"public_key": "some_public_key", "private_key": "some_private_key"},
    ],
}


SAMPLE_CREDENTIALS = {
    "exploit_user_list": ["user1", "user3"],
    "exploit_password_list": ["abcdefg", "root"],
    "exploit_ssh_keys": [{"public_key": "some_public_key", "private_key": "some_private_key"}],
    "exploit_ntlm_hash_list": [],
}


@pytest.fixture
def aggregating_credentials_store() -> AggregatingCredentialsStore:
    return AggregatingCredentialsStore()


@pytest.mark.parametrize("credentials_to_store", [DEFAULT_CREDENTIALS, SAMPLE_CREDENTIALS])
def test_get_credentials_from_store(aggregating_credentials_store, credentials_to_store):
    get_updated_credentials_for_propagation = MagicMock(return_value=credentials_to_store)

    aggregating_credentials_store.get_credentials(get_updated_credentials_for_propagation)

    assert aggregating_credentials_store.stored_credentials == credentials_to_store


def test_add_credentials_to_empty_store(aggregating_credentials_store):

    aggregating_credentials_store.add_credentials(SAMPLE_CREDENTIALS)

    assert aggregating_credentials_store.stored_credentials == SAMPLE_CREDENTIALS


def test_add_credentials_to_full_store(aggregating_credentials_store):
    get_updated_credentials_for_propagation = MagicMock(return_value=DEFAULT_CREDENTIALS)

    aggregating_credentials_store.get_credentials(get_updated_credentials_for_propagation)

    aggregating_credentials_store.add_credentials(SAMPLE_CREDENTIALS)

    actual_stored_credentials = aggregating_credentials_store.stored_credentials

    assert actual_stored_credentials["exploit_user_list"] == [
        "Administrator",
        "root",
        "user1",
        "user3",
    ]
    assert actual_stored_credentials["exploit_password_list"] == [
        "123456",
        "123456789",
        "abcdefg",
        "password",
        "root",
    ]
    assert actual_stored_credentials["exploit_ssh_keys"] == DEFAULT_CREDENTIALS["exploit_ssh_keys"]
