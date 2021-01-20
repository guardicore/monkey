import mongoengine
import pytest

from monkey_island.cc.models import Monkey
from monkey_island.cc.models.edge import Edge
from monkey_island.cc.models.zero_trust.finding import Finding


@pytest.fixture(scope='session', autouse=True)
def change_to_mongo_mock():
    # Make sure tests are working with mongomock
    mongoengine.disconnect()
    mongoengine.connect('mongoenginetest', host='mongomock://localhost')


@pytest.fixture(scope='function')
def uses_database():
    _clean_edge_db()
    _clean_monkey_db()
    _clean_finding_db()


def _clean_monkey_db():
    Monkey.objects().delete()


def _clean_edge_db():
    Edge.objects().delete()


def _clean_finding_db():
    Finding.objects().delete()
