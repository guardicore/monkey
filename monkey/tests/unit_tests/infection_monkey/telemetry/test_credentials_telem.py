import json

import pytest

from infection_monkey.credential_collectors import Password, SSHKeypair, Username
from infection_monkey.i_puppet import Credentials
from infection_monkey.telemetry.credentials_telem import CredentialsTelem

USERNAME = "m0nkey"
PASSWORD = "mmm"
PUBLIC_KEY = "pub_key"
PRIVATE_KEY = "priv_key"


@pytest.fixture
def credentials_for_test():

    return Credentials(
        [Username(USERNAME)], [Password(PASSWORD), SSHKeypair(PRIVATE_KEY, PUBLIC_KEY)]
    )


def test_credential_telem_send(spy_send_telemetry, credentials_for_test):

    expected_data = [
        {
            "identities": [{"username": USERNAME, "credential_type": "USERNAME"}],
            "secrets": [
                {"password": PASSWORD, "credential_type": "PASSWORD"},
                {
                    "private_key": PRIVATE_KEY,
                    "public_key": PUBLIC_KEY,
                    "credential_type": "SSH_KEYPAIR",
                },
            ],
        }
    ]

    telem = CredentialsTelem([credentials_for_test])
    telem.send()

    expected_data = json.dumps(expected_data, cls=telem.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "credentials"


def test_credentials_property(credentials_for_test):
    telem = CredentialsTelem([credentials_for_test])

    assert len(list(telem.credentials)) == 1
    assert list(telem.credentials)[0] == credentials_for_test
