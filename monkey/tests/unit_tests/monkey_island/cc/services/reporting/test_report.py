import datetime
from copy import deepcopy

import mongoengine
import pytest
from bson import ObjectId

from monkey_island.cc.models.telemetries import save_telemetry
from monkey_island.cc.services.reporting.report import ReportService

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
        },
    },
}

SYSTEM_INFO_TELEMETRY_TELEM = {
    "_id": TELEM_ID["system_info_creds"],
    "monkey_guid": MONKEY_GUID,
    "telem_category": "system_info",
    "timestamp": datetime.datetime(2021, 2, 19, 9, 0, 14, 984000),
    "command_control_channel": {
        "src": "192.168.56.1",
        "dst": "192.168.56.2",
    },
    "data": {
        "credentials": {
            USER: {
                "password": PWD,
                "lm_hash": LM_HASH,
                "ntlm_hash": NT_HASH,
            }
        }
    },
}

NO_CREDS_TELEMETRY_TELEM = {
    "_id": TELEM_ID["no_creds"],
    "monkey_guid": MONKEY_GUID,
    "telem_category": "exploit",
    "timestamp": datetime.datetime(2021, 2, 19, 9, 0, 14, 984000),
    "command_control_channel": {
        "src": "192.168.56.1",
        "dst": "192.168.56.2",
    },
    "data": {
        "machine": {
            "ip_addr": VICTIM_IP,
            "domain_name": VICTIM_DOMAIN_NAME,
        },
        "info": {"credentials": {}},
    },
}

MONKEY_TELEM = {"_id": TELEM_ID["monkey"], "guid": MONKEY_GUID, "hostname": HOSTNAME}

NODE_DICT = {
    "id": "602f62118e30cf35830ff8e4",
    "label": "WinDev2010Eval.mshome.net",
    "group": "monkey_windows",
    "os": "windows",
    "dead": True,
    "exploits": [
        {
            "exploitation_result": True,
            "exploiter": "DrupalExploiter",
            "info": {
                "display_name": "Drupal Server",
                "started": datetime.datetime(2021, 2, 19, 9, 0, 14, 950000),
                "finished": datetime.datetime(2021, 2, 19, 9, 0, 14, 950000),
                "vulnerable_urls": [],
                "vulnerable_ports": [],
                "executed_cmds": [],
            },
            "attempts": [],
            "timestamp": datetime.datetime(2021, 2, 19, 9, 0, 14, 984000),
            "origin": "MonkeyIsland : 192.168.56.1",
        },
        {
            "exploitation_result": True,
            "exploiter": "ElasticGroovyExploiter",
            "info": {
                "display_name": "Elastic search",
                "started": datetime.datetime(2021, 2, 19, 9, 0, 15, 16000),
                "finished": datetime.datetime(2021, 2, 19, 9, 0, 15, 17000),
                "vulnerable_urls": [],
                "vulnerable_ports": [],
                "executed_cmds": [],
            },
            "attempts": [],
            "timestamp": datetime.datetime(2021, 2, 19, 9, 0, 15, 60000),
            "origin": "MonkeyIsland : 192.168.56.1",
        },
    ],
}

NODE_DICT_DUPLICATE_EXPLOITS = deepcopy(NODE_DICT)
NODE_DICT_DUPLICATE_EXPLOITS["exploits"][1] = NODE_DICT_DUPLICATE_EXPLOITS["exploits"][0]

NODE_DICT_FAILED_EXPLOITS = deepcopy(NODE_DICT)
NODE_DICT_FAILED_EXPLOITS["exploits"][0]["exploitation_result"] = False
NODE_DICT_FAILED_EXPLOITS["exploits"][1]["exploitation_result"] = False


@pytest.fixture
def fake_mongo(monkeypatch):
    mongo = mongoengine.connection.get_connection()
    monkeypatch.setattr("monkey_island.cc.services.reporting.report.mongo", mongo)
    monkeypatch.setattr("monkey_island.cc.models.telemetries.telemetry_dal.mongo", mongo)
    monkeypatch.setattr("monkey_island.cc.services.node.mongo", mongo)
    return mongo


@pytest.mark.usefixtures("uses_database")
def test_get_stolen_creds_exploit(fake_mongo):
    fake_mongo.db.telemetry.insert_one(EXPLOIT_TELEMETRY_TELEM)

    stolen_creds_exploit = ReportService.get_stolen_creds()
    expected_stolen_creds_exploit = [
        {"origin": VICTIM_DOMAIN_NAME, "type": "LM hash", "username": USER},
        {"origin": VICTIM_DOMAIN_NAME, "type": "NTLM hash", "username": USER},
    ]

    assert expected_stolen_creds_exploit == stolen_creds_exploit


@pytest.mark.slow
@pytest.mark.usefixtures("uses_database", "uses_encryptor")
def test_get_stolen_creds_system_info(fake_mongo):
    fake_mongo.db.monkey.insert_one(MONKEY_TELEM)
    save_telemetry(SYSTEM_INFO_TELEMETRY_TELEM)

    stolen_creds_system_info = ReportService.get_stolen_creds()
    expected_stolen_creds_system_info = [
        {"origin": HOSTNAME, "type": "Clear Password", "username": USER},
        {"origin": HOSTNAME, "type": "LM hash", "username": USER},
        {"origin": HOSTNAME, "type": "NTLM hash", "username": USER},
    ]

    assert expected_stolen_creds_system_info == stolen_creds_system_info


@pytest.mark.usefixtures("uses_database")
def test_get_stolen_creds_no_creds(fake_mongo):
    fake_mongo.db.monkey.insert_one(MONKEY_TELEM)
    save_telemetry(NO_CREDS_TELEMETRY_TELEM)

    stolen_creds_no_creds = ReportService.get_stolen_creds()
    expected_stolen_creds_no_creds = []

    assert expected_stolen_creds_no_creds == stolen_creds_no_creds
