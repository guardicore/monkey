from datetime import datetime

import mongoengine
import pytest

from monkey_island.cc.services.config import ConfigService


@pytest.fixture
def fake_mongo(monkeypatch):
    mongo = mongoengine.connection.get_connection()
    monkeypatch.setattr("monkey_island.cc.services.config.mongo", mongo)
    config = ConfigService.get_default_config()
    ConfigService.update_config(config, should_encrypt=True)


CREDENTIAL_TELEM_TEMPLATE = {
    "monkey_guid": "272405690278083",
    "telem_category": "credentials",
    "timestamp": datetime(2022, 2, 18, 11, 51, 15, 338953),
    "command_control_channel": {"src": "10.2.2.251", "dst": "10.2.2.251:5000"},
    "data": None,
}
