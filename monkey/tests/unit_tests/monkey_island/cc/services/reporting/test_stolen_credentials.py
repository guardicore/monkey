import pytest

from common.credentials import CredentialComponentType
from monkey_island.cc.models import Monkey, StolenCredentials
from monkey_island.cc.services.reporting.stolen_credentials import get_stolen_creds

monkey_hostname = "fake_hostname"
fake_monkey_guid = "abc"

fake_username = "m0nk3y_user"
fake_nt_hash = "c1c58f96cdf212b50837bc11a00be47c"
fake_lm_hash = "299BD128C1101FD6"
fake_password = "trytostealthis"
fake_ssh_key = "RSA_fake_key"
fake_credentials = {
    "identities": [{"username": fake_username, "credential_type": "USERNAME"}],
    "secrets": [
        CredentialComponentType.NT_HASH.name,
        CredentialComponentType.LM_HASH.name,
        CredentialComponentType.PASSWORD.name,
        CredentialComponentType.SSH_KEYPAIR.name,
    ],
}


@pytest.fixture
def fake_monkey():
    monkey = Monkey()
    monkey.guid = fake_monkey_guid
    monkey.hostname = monkey_hostname
    monkey.save()
    return monkey.id


@pytest.mark.usefixtures("uses_database")
def test_get_credentials(fake_monkey):
    StolenCredentials(
        identities=fake_credentials["identities"],
        secrets=fake_credentials["secrets"],
        monkey=fake_monkey,
    ).save()

    credentials = get_stolen_creds()

    result1 = {
        "origin": monkey_hostname,
        "_type": CredentialComponentType.NT_HASH.name,
        "type": "NTLM hash",
        "username": fake_username,
    }
    result2 = {
        "origin": monkey_hostname,
        "_type": CredentialComponentType.LM_HASH.name,
        "type": "LM hash",
        "username": fake_username,
    }
    result3 = {
        "origin": monkey_hostname,
        "_type": CredentialComponentType.PASSWORD.name,
        "type": "Clear Password",
        "username": fake_username,
    }
    result4 = {
        "origin": monkey_hostname,
        "_type": CredentialComponentType.SSH_KEYPAIR.name,
        "type": "Clear SSH private key",
        "username": fake_username,
    }
    assert result1 in credentials
    assert result2 in credentials
    assert result3 in credentials
    assert result4 in credentials
