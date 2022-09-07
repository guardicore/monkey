import json

import pytest

from common.credentials import Credentials, Password, Username
from infection_monkey.telemetry.credentials_telem import CredentialsTelem

USERNAME = "m0nkey"
PASSWORD = "mmm"
PUBLIC_KEY = "pub_key"
PRIVATE_KEY = "priv_key"


@pytest.fixture
def credentials_for_test():
    return Credentials(identity=Username(username=USERNAME), secret=Password(password=PASSWORD))


def test_credential_telem_send(spy_send_telemetry, credentials_for_test):

    expected_data = [credentials_for_test.dict(simplify=True)]

    telem = CredentialsTelem([credentials_for_test])
    telem.send()

    assert json.loads(spy_send_telemetry.data) == expected_data
    assert spy_send_telemetry.telem_category == "credentials"


def test_credentials_property(credentials_for_test):
    telem = CredentialsTelem([credentials_for_test])

    assert len(list(telem.credentials)) == 1
    assert list(telem.credentials)[0] == credentials_for_test
