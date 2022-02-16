import json

from infection_monkey.credential_collectors import Password, SSHKeypair, Username
from infection_monkey.i_puppet import Credentials
from infection_monkey.telemetry.credentials_telem import CredentialsTelem


def test_credential_telem_send(spy_send_telemetry):
    username = "m0nkey"
    password = "mmm"
    public_key = "pub_key"
    private_key = "priv_key"

    expected_data = [
        {
            "identities": [{"username": username, "credential_type": "USERNAME"}],
            "secrets": [
                {"password": password, "credential_type": "PASSWORD"},
                {
                    "private_key": "pub_key",
                    "public_key": "priv_key",
                    "credential_type": "SSH_KEYPAIR",
                },
            ],
        }
    ]

    credentials = Credentials(
        [Username(username)], [Password(password), SSHKeypair(public_key, private_key)]
    )

    telem = CredentialsTelem([credentials])
    telem.send()

    expected_data = json.dumps(expected_data, cls=telem.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "credentials"
