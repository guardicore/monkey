import pytest
from tests.unit_tests.monkey_island.cc.mongomock_fixtures import *  # noqa: F401,F403,E402

from monkey_island.cc.server_utils.encryption import unlock_datastore_encryptor


@pytest.fixture
def uses_encryptor(data_for_tests_dir):
    secret = "m0nk3y_u53r:3cr3t_p455w0rd"
    unlock_datastore_encryptor(data_for_tests_dir, secret)
