from copy import deepcopy
from datetime import datetime

import mongoengine
import pytest

from monkey_island.cc.models.telemetries import get_telemetry_by_query, save_telemetry
from monkey_island.cc.models.telemetries.telemetry import Telemetry

MOCK_CREDENTIALS = {
    "M0nk3y": {
        "username": "M0nk3y",
        "password": "",
        "ntlm_hash": "e87f2f73e353f1d95e42ce618601b61f",
        "lm_hash": "",
    },
    "user": {"username": "user", "password": "test", "ntlm_hash": "", "lm_hash": ""},
}

MOCK_DATA_DICT = {
    "network_info": {},
    "credentials": deepcopy(MOCK_CREDENTIALS),
}

MOCK_TELEMETRY = {
    "timestamp": datetime.now(),
    "command_control_channel": {
        "src": "192.168.56.1",
        "dst": "192.168.56.2",
    },
    "monkey_guid": "211375648895908",
    "telem_category": "system_info",
    "data": MOCK_DATA_DICT,
}

MOCK_NO_ENCRYPTION_NEEDED_TELEMETRY = {
    "timestamp": datetime.now(),
    "command_control_channel": {
        "src": "192.168.56.1",
        "dst": "192.168.56.2",
    },
    "monkey_guid": "211375648895908",
    "telem_category": "state",
    "data": {"done": False},
}


@pytest.fixture(autouse=True)
def fake_mongo(monkeypatch):
    mongo = mongoengine.connection.get_connection()
    monkeypatch.setattr("monkey_island.cc.models.telemetries.telemetry_dal.mongo", mongo)


@pytest.mark.slow
@pytest.mark.usefixtures("uses_database", "uses_encryptor")
def test_telemetry_encryption():
    secret_keys = ["password", "lm_hash", "ntlm_hash"]

    save_telemetry(MOCK_TELEMETRY)

    encrypted_telemetry = Telemetry.objects.first()
    for user in MOCK_CREDENTIALS.keys():
        assert encrypted_telemetry["data"]["credentials"][user]["username"] == user

        for s in secret_keys:
            assert encrypted_telemetry["data"]["credentials"][user][s] != MOCK_CREDENTIALS[user][s]

    decrypted_telemetry = get_telemetry_by_query({})[0]
    for user in MOCK_CREDENTIALS.keys():
        assert decrypted_telemetry["data"]["credentials"][user]["username"] == user

        for s in secret_keys:
            assert decrypted_telemetry["data"]["credentials"][user][s] == MOCK_CREDENTIALS[user][s]


@pytest.mark.slow
@pytest.mark.usefixtures("uses_database", "uses_encryptor")
def test_no_encryption_needed():
    # Make sure telemetry save doesn't break when telemetry doesn't need encryption
    save_telemetry(MOCK_NO_ENCRYPTION_NEEDED_TELEMETRY)
