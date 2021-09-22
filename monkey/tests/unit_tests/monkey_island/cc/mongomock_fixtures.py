import mongoengine
import pytest

MOCK_DB_NAME = "mongoenginetest"


@pytest.fixture(scope="module", autouse=True)
def change_to_mongo_mock():
    # Make sure tests are working with mongomock
    mongoengine.disconnect()
    mongoengine.connect(MOCK_DB_NAME, host="mongomock://localhost")


@pytest.fixture(scope="function")
def uses_database():
    _drop_database()


def _drop_database():
    mongoengine.connection.get_connection().drop_database(MOCK_DB_NAME)
