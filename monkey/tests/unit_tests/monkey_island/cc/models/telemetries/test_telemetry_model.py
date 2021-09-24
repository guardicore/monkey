from copy import deepcopy
from datetime import datetime

import mongoengine
import pytest

from monkey_island.cc.models.telemetries import Telemetry
from monkey_island.cc.models.utils.document_encryptor import SensitiveField
from monkey_island.cc.models.utils.field_encryptors.mimikatz_results_encryptor import (
    MimikatzResultsEncryptor,
)

MOCK_CREDENTIALS = {
    "Vakaris": {
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
    "mimikatz": deepcopy(MOCK_CREDENTIALS),
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

MOCK_SENSITIVE_FIELDS = [
    SensitiveField("data.credentials", MimikatzResultsEncryptor),
    SensitiveField("data.mimikatz", MimikatzResultsEncryptor),
]


@pytest.fixture(autouse=True)
def patch_sensitive_fields(monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.models.telemetries.telemetry.sensitive_fields",
        MOCK_SENSITIVE_FIELDS,
    )


@pytest.fixture(autouse=True)
def fake_mongo(monkeypatch):
    mongo = mongoengine.connection.get_connection()
    monkeypatch.setattr("monkey_island.cc.models.telemetries.telemetry.mongo", mongo)


@pytest.mark.usefixtures("uses_database", "uses_encryptor")
def test_telemetry_encryption(monkeypatch):

    Telemetry.save_telemetry(MOCK_TELEMETRY)
    assert (
        not Telemetry.objects.first()["data"]["credentials"]["user"]["password"]
        == MOCK_CREDENTIALS["user"]["password"]
    )
    assert (
        not Telemetry.objects.first()["data"]["mimikatz"]["Vakaris"]["ntlm_hash"]
        == MOCK_CREDENTIALS["Vakaris"]["ntlm_hash"]
    )
    assert (
        Telemetry.get_telemetry_by_query({})[0]["data"]["credentials"]["user"]["password"]
        == MOCK_CREDENTIALS["user"]["password"]
    )
    assert (
        Telemetry.get_telemetry_by_query({})[0]["data"]["mimikatz"]["Vakaris"]["ntlm_hash"]
        == MOCK_CREDENTIALS["Vakaris"]["ntlm_hash"]
    )


@pytest.mark.usefixtures("uses_database", "uses_encryptor")
def test_no_encryption_needed(monkeypatch, data_for_tests_dir):
    # Make sure telemetry save doesn't break when telemetry doesn't need encryption
    Telemetry.save_telemetry(MOCK_NO_ENCRYPTION_NEEDED_TELEMETRY)
