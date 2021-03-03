import mongomock
import pytest
from bson import ObjectId

import monkey_island.cc.database

TELEM_ID = {
    "exploit_creds": ObjectId(b"123456789000"),
    "system_info_creds": ObjectId(b"987654321000"),
    "no_creds": ObjectId(b"112233445566"),
    "monkey": ObjectId(b"665544332211"),
}
MONKEY_GUID = "67890"
USER = "user-name"
PWD = "password123"
LM_HASH = "e52cac67419a9a22664345140a852f61"
NT_HASH = "a9fdfa038c4b75ebc76dc855dd74f0da"
VICTIM_IP = "0.0.0.0"
VICTIM_DOMAIN_NAME = "domain-name"
HOSTNAME = "name-of-host"
EXPLOITER_CLASS_NAME = "exploiter-name"

# Below telem constants only contain fields relevant to current tests

EXPLOIT_TELEMETRY_TELEM = {
    "_id": TELEM_ID["exploit_creds"],
    "monkey_guid": MONKEY_GUID,
    "telem_category": "exploit",
    "data": {
        "machine": {
            "ip_addr": VICTIM_IP,
            "domain_name": VICTIM_DOMAIN_NAME,
        },
        "info": {
            "credentials": {
                USER: {
                    "username": USER,
                    "lm_hash": LM_HASH,
                    "ntlm_hash": NT_HASH,
                }
            }
        }
    }
}


SYSTEM_INFO_TELEMETRY_TELEM = {
    "_id": TELEM_ID["system_info_creds"],
    "monkey_guid": MONKEY_GUID,
    "telem_category": "system_info",
    "data": {
        "credentials": {
            USER: {
                "password": PWD,
                "lm_hash": LM_HASH,
                "ntlm_hash": NT_HASH,
            }
        }
    }
}

NO_CREDS_TELEMETRY_TELEM = {
    "_id": TELEM_ID["no_creds"],
    "monkey_guid": MONKEY_GUID,
    "telem_category": "exploit",
    "data": {
        "machine": {
            "ip_addr": VICTIM_IP,
            "domain_name": VICTIM_DOMAIN_NAME,
        },
        "info": {"credentials": {}}
    }
}

MONKEY_TELEM = {"_id": TELEM_ID["monkey"], "guid": MONKEY_GUID, "hostname": HOSTNAME}


@pytest.fixture
def fake_mongo(monkeypatch):
    mongo = mongomock.MongoClient()
    monkeypatch.setattr("monkey_island.cc.database.mongo", mongo)
    return mongo


@pytest.fixture
def report_service():
    # can't be imported before monkeypatching since mongo connection is made at module level
    # see https://stackoverflow.com/a/51994349/
    from monkey_island.cc.services.reporting.report import ReportService

    return ReportService


def test_get_stolen_creds_exploit(fake_mongo, report_service):
    fake_mongo.db.telemetry.insert_one(EXPLOIT_TELEMETRY_TELEM)

    stolen_creds_exploit = report_service.get_stolen_creds()
    expected_stolen_creds_exploit = [
        {"origin": VICTIM_DOMAIN_NAME, "type": "LM hash", "username": USER},
        {"origin": VICTIM_DOMAIN_NAME, "type": "NTLM hash", "username": USER},
    ]

    assert expected_stolen_creds_exploit == stolen_creds_exploit


def test_get_stolen_creds_system_info(fake_mongo, report_service):
    fake_mongo.db.monkey.insert_one(MONKEY_TELEM)
    fake_mongo.db.telemetry.insert_one(SYSTEM_INFO_TELEMETRY_TELEM)

    expected_stolen_creds_system_info = [
        {"origin": HOSTNAME, "type": "Clear Password", "username": USER},
        {"origin": HOSTNAME, "type": "LM hash", "username": USER},
        {"origin": HOSTNAME, "type": "NTLM hash", "username": USER},
    ]

    assert expected_stolen_creds_system_info == stolen_creds_system_info


def test_get_stolen_creds_no_creds(fake_mongo, report_service):
    fake_mongo.db.telemetry.insert_one(NO_CREDS_TELEMETRY_TELEM)

    stolen_creds_no_creds = report_service.get_stolen_creds()
    expected_stolen_creds_no_creds = []

    assert expected_stolen_creds_no_creds == stolen_creds_no_creds
