from copy import deepcopy
from datetime import datetime

import mongoengine
import pytest

from monkey_island.cc.models.telemetries import save_telemetry

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
    "monkey_guid": "211375648895908",
    "telem_category": "system_info",
    "data": MOCK_DATA_DICT,
}

MOCK_NO_ENCRYPTION_NEEDED_TELEMETRY = {
    "timestamp": datetime.now(),
    "monkey_guid": "211375648895908",
    "telem_category": "state",
    "data": {"done": False},
}


@pytest.fixture(autouse=True)
def fake_mongo(monkeypatch):
    mongo = mongoengine.connection.get_connection()
    monkeypatch.setattr("monkey_island.cc.models.telemetries.telemetry_dal.mongo", mongo)


@pytest.mark.slow
@pytest.mark.usefixtures("uses_database")
def test_no_encryption_needed():
    # Make sure telemetry save doesn't break when telemetry doesn't need encryption
    save_telemetry(MOCK_NO_ENCRYPTION_NEEDED_TELEMETRY)
