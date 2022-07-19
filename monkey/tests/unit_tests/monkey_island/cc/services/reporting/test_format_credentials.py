from common.credentials import (
    CredentialComponentType,
    Credentials,
    LMHash,
    NTHash,
    Password,
    SSHKeypair,
    Username,
)
from monkey_island.cc.services.reporting import format_creds_for_reporting

monkey_hostname = "fake_hostname"
fake_monkey_guid = "abc"

fake_username = Username("m0nk3y_user")
fake_nt_hash = NTHash("AEBD4DE384C7EC43AAD3B435B51404EE")
fake_lm_hash = LMHash("7A21990FCD3D759941E45C490F143D5F")
fake_password = Password("trytostealthis")
fake_ssh_public_key = "RSA_public_key"
fake_ssh_private_key = "RSA_private_key"
fake_ssh_key = SSHKeypair(fake_ssh_private_key, fake_ssh_public_key)

identities = (fake_username,)
secrets = (fake_nt_hash, fake_lm_hash, fake_password, fake_ssh_key)

fake_credentials = [
    Credentials(fake_username, fake_nt_hash),
    Credentials(fake_username, fake_lm_hash),
    Credentials(fake_username, fake_password),
    Credentials(fake_username, fake_ssh_key),
    Credentials(None, fake_ssh_key),
    Credentials(fake_username, None),
]


def test_formatting_credentials_for_report():

    credentials = format_creds_for_reporting(fake_credentials)

    result1 = {
        "_type": CredentialComponentType.NT_HASH.name,
        "type": "NTLM hash",
        "username": fake_username.username,
    }
    result2 = {
        "_type": CredentialComponentType.LM_HASH.name,
        "type": "LM hash",
        "username": fake_username.username,
    }
    result3 = {
        "_type": CredentialComponentType.PASSWORD.name,
        "type": "Clear Password",
        "username": fake_username.username,
    }
    result4 = {
        "_type": CredentialComponentType.SSH_KEYPAIR.name,
        "type": "Clear SSH private key",
        "username": fake_username.username,
    }
    result5 = {
        "_type": CredentialComponentType.SSH_KEYPAIR.name,
        "type": "Clear SSH private key",
        "username": "",
    }
    assert result1 in credentials
    assert result2 in credentials
    assert result3 in credentials
    assert result4 in credentials
    assert result5 in credentials
