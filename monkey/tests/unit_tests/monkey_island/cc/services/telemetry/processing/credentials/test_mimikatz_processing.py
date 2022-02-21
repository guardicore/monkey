from copy import deepcopy
from datetime import datetime

import dpath.util
import mongoengine
import pytest

from common.config_value_paths import (
    LM_HASH_LIST_PATH,
    NTLM_HASH_LIST_PATH,
    PASSWORD_LIST_PATH,
    USER_LIST_PATH,
)
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.telemetry.processing.credentials.credentials_parser import (
    parse_credentials,
)

MIMIKATZ_TELEM_TEMPLATE = {
    "monkey_guid": "272405690278083",
    "telem_category": "credentials",
    "timestamp": datetime(2022, 2, 18, 11, 51, 15, 338953),
    "command_control_channel": {"src": "10.2.2.251", "dst": "10.2.2.251:5000"},
    "data": None,
}

fake_username = "m0nk3y_user"
mimikatz_telem_usernames = deepcopy(MIMIKATZ_TELEM_TEMPLATE)
mimikatz_telem_usernames["data"] = [
    {"identities": [{"username": fake_username, "credential_type": "username"}], "secrets": []}
]

fake_nt_hash = "c1c58f96cdf212b50837bc11a00be47c"
fake_lm_hash = "299BD128C1101FD6"
fake_password = "trytostealthis"
mimikatz_telem = deepcopy(MIMIKATZ_TELEM_TEMPLATE)
mimikatz_telem["data"] = [
    {
        "identities": [{"username": fake_username, "credential_type": "username"}],
        "secrets": [
            {"nt_hash": fake_nt_hash, "credential_type": "nt_hash"},
            {"lm_hash": fake_lm_hash, "credential_type": "lm_hash"},
            {"password": fake_password, "credential_type": "password"},
        ],
    }
]

mimikatz_empty_telem = deepcopy(MIMIKATZ_TELEM_TEMPLATE)
mimikatz_empty_telem["data"] = [{"identities": [], "secrets": []}]


@pytest.fixture
def fake_mongo(monkeypatch):
    mongo = mongoengine.connection.get_connection()
    monkeypatch.setattr("monkey_island.cc.services.config.mongo", mongo)
    config = ConfigService.get_default_config()
    ConfigService.update_config(config, should_encrypt=True)
    return mongo


@pytest.mark.usefixtures("uses_database")
def test_mimikatz_username_parsing(fake_mongo):
    parse_credentials(mimikatz_telem_usernames)
    config = ConfigService.get_config(should_decrypt=True)
    assert fake_username in dpath.util.get(config, USER_LIST_PATH)


@pytest.mark.usefixtures("uses_database")
def test_mimikatz_telemetry_parsing(fake_mongo):
    parse_credentials(mimikatz_telem)
    config = ConfigService.get_config(should_decrypt=True)
    assert fake_username in dpath.util.get(config, USER_LIST_PATH)
    assert fake_nt_hash in dpath.util.get(config, NTLM_HASH_LIST_PATH)
    assert fake_lm_hash in dpath.util.get(config, LM_HASH_LIST_PATH)
    assert fake_password in dpath.util.get(config, PASSWORD_LIST_PATH)


@pytest.mark.usefixtures("uses_database")
def test_empty_mimikatz_telemetry_parsing(fake_mongo):
    default_config = deepcopy(ConfigService.get_config(should_decrypt=True))
    default_usernames = dpath.util.get(default_config, USER_LIST_PATH)
    default_nt_hashes = dpath.util.get(default_config, NTLM_HASH_LIST_PATH)
    default_lm_hashes = dpath.util.get(default_config, LM_HASH_LIST_PATH)
    default_passwords = dpath.util.get(default_config, PASSWORD_LIST_PATH)

    parse_credentials(mimikatz_empty_telem)
    config = ConfigService.get_config(should_decrypt=True)

    assert default_usernames == dpath.util.get(config, USER_LIST_PATH)
    assert default_nt_hashes == dpath.util.get(config, NTLM_HASH_LIST_PATH)
    assert default_lm_hashes == dpath.util.get(config, LM_HASH_LIST_PATH)
    assert default_passwords == dpath.util.get(config, PASSWORD_LIST_PATH)
