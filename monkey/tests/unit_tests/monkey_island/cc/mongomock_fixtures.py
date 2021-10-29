import mongoengine
import pytest

# Database name has to match the db used in the codebase,
# else the name needs to be mocked during tests.
# Currently its used like so: "mongo.db.telemetry.find()".
MOCK_DB_NAME = "db"


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
