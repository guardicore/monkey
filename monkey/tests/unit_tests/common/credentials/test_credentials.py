import logging
from pathlib import Path

import pytest
from monkeytypes import InfectionMonkeyBaseModel
from pydantic import SecretBytes
from pydantic.types import SecretStr
from tests.data_for_tests.propagation_credentials import (
    CREDENTIALS,
    CREDENTIALS_DICTS,
    LM_HASH,
    PASSWORD_1,
    PLAINTEXT_LM_HASH,
    PLAINTEXT_PASSWORD,
    PLAINTEXT_PRIVATE_KEY_1,
    PRIVATE_KEY_1,
)

from common.credentials import Credentials, get_plaintext


@pytest.mark.parametrize(
    "credentials, expected_credentials_dict", zip(CREDENTIALS, CREDENTIALS_DICTS)
)
def test_credentials_serialization_json(credentials, expected_credentials_dict):
    serialized_credentials = credentials.json()
    deserialized_credentials = Credentials.parse_raw(serialized_credentials)

    assert credentials == deserialized_credentials


logger = logging.getLogger()
logger.level = logging.DEBUG


def test_credentials_secrets_not_logged(caplog):
    class TestSecret(InfectionMonkeyBaseModel):
        some_secret: SecretStr
        some_secret_in_bytes: SecretBytes

    class TestCredentials(Credentials):
        secret: TestSecret

    sensitive = "super_secret"
    creds = TestCredentials(
        identity=None,
        secret=TestSecret(some_secret=sensitive, some_secret_in_bytes=sensitive.encode()),
    )

    logging.getLogger().info(
        f"{creds.secret.some_secret} and" f" {creds.secret.some_secret_in_bytes}"
    )

    assert sensitive not in caplog.text


_plaintext = [
    PLAINTEXT_PASSWORD,
    PLAINTEXT_PRIVATE_KEY_1,
    PLAINTEXT_LM_HASH,
    "",
    "already_plaintext",
    Path("C:\\jolly_fella"),
    None,
]
_hidden = [
    PASSWORD_1,
    PRIVATE_KEY_1,
    LM_HASH,
    "",
    "already_plaintext",
    Path("C:\\jolly_fella"),
    None,
]


@pytest.mark.parametrize("expected, hidden", list(zip(_plaintext, _hidden)))
def test_get_plain_text(expected, hidden):
    assert expected == get_plaintext(hidden)
