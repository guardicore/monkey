import pytest

from monkey_island.cc.setup.mongo import mongo_setup


def test_connect_to_mongodb_timeout(monkeypatch):
    monkeypatch.setattr(mongo_setup, "_is_db_server_up", lambda _: False)
    with pytest.raises(mongo_setup.MongoDBTimeOutError):
        mongo_setup.connect_to_mongodb(0.0000000001)


def test_connect_to_mongodb_version_too_old(monkeypatch):
    monkeypatch.setattr(mongo_setup, "_is_db_server_up", lambda _: True)
    monkeypatch.setattr(mongo_setup, "_get_db_version", lambda _: ("1", "0", "0"))
    with pytest.raises(mongo_setup.MongoDBVersionError):
        mongo_setup.connect_to_mongodb(0)
