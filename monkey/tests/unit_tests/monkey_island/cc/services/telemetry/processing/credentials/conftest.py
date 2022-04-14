from datetime import datetime

import mongoengine
import pytest

from monkey_island.cc.models import Monkey
from monkey_island.cc.services.config import ConfigService

fake_monkey_guid = "272405690278083"
fake_ip_address = "192.168.56.1"


@pytest.fixture
def fake_mongo(monkeypatch, uses_encryptor):
    mongo = mongoengine.connection.get_connection()
    monkeypatch.setattr("monkey_island.cc.services.config.mongo", mongo)
    config = ConfigService.get_default_config()
    ConfigService.update_config(config, should_encrypt=True)


@pytest.fixture
def insert_fake_monkey():
    monkey = Monkey(guid=fake_monkey_guid, ip_addresses=[fake_ip_address])
    monkey.save()


CREDENTIAL_TELEM_TEMPLATE = {
    "monkey_guid": "272405690278083",
    "telem_category": "credentials",
    "timestamp": datetime(2022, 2, 18, 11, 51, 15, 338953),
    "command_control_channel": {"src": "10.2.2.251", "dst": "10.2.2.251:5000"},
    "data": None,
}
