import pytest
from tests.data_for_tests.propagation_credentials import CREDENTIALS, CREDENTIALS_DICTS

from common.credentials import Credentials


@pytest.mark.parametrize(
    "credentials, expected_credentials_dict", zip(CREDENTIALS, CREDENTIALS_DICTS)
)
def test_credentials_serialization_json(credentials, expected_credentials_dict):
    serialized_credentials = credentials.json()
    deserialized_credentials = Credentials.parse_raw(serialized_credentials)

    assert credentials == deserialized_credentials
