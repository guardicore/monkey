import logging

import pytest
from pydantic import SecretBytes
from pydantic.types import SecretStr
from tests.data_for_tests.propagation_credentials import CREDENTIALS, CREDENTIALS_DICTS

from common.base_models import InfectionMonkeyBaseModel
from common.credentials import Credentials


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
