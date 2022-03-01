from copy import deepcopy

import dpath.util
import pytest
from tests.unit_tests.monkey_island.cc.services.telemetry.processing.credentials.conftest import (
    CREDENTIAL_TELEM_TEMPLATE,
)

from common.common_consts.credential_component_type import CredentialComponentType
from common.config_value_paths import (
    LM_HASH_LIST_PATH,
    NTLM_HASH_LIST_PATH,
    PASSWORD_LIST_PATH,
    USER_LIST_PATH,
)
from monkey_island.cc.models import StolenCredentials
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.telemetry.processing.credentials.credentials_parser import (
    parse_credentials,
)

fake_username = "m0nk3y_user"
cred_telem_usernames = deepcopy(CREDENTIAL_TELEM_TEMPLATE)
cred_telem_usernames["data"] = [
    {"identities": [{"username": fake_username, "credential_type": "USERNAME"}], "secrets": []}
]

fake_special_username = "$m0nk3y.user"
cred_telem_special_usernames = deepcopy(CREDENTIAL_TELEM_TEMPLATE)
cred_telem_special_usernames["data"] = [
    {
        "identities": [{"username": fake_special_username, "credential_type": "USERNAME"}],
        "secrets": [],
    }
]

fake_nt_hash = "c1c58f96cdf212b50837bc11a00be47c"
fake_lm_hash = "299BD128C1101FD6"
fake_password = "trytostealthis"
cred_telem = deepcopy(CREDENTIAL_TELEM_TEMPLATE)
cred_telem["data"] = [
    {
        "identities": [{"username": fake_username, "credential_type": "USERNAME"}],
        "secrets": [
            {"nt_hash": fake_nt_hash, "credential_type": "NT_HASH"},
            {"lm_hash": fake_lm_hash, "credential_type": "LM_HASH"},
            {"password": fake_password, "credential_type": "PASSWORD"},
        ],
    }
]

cred_empty_telem = deepcopy(CREDENTIAL_TELEM_TEMPLATE)
cred_empty_telem["data"] = [{"identities": [], "secrets": []}]


@pytest.mark.slow
@pytest.mark.usefixtures("uses_database", "fake_mongo", "insert_fake_monkey")
def test_cred_username_parsing():
    parse_credentials(cred_telem_usernames)
    config = ConfigService.get_config(should_decrypt=True)
    assert fake_username in dpath.util.get(config, USER_LIST_PATH)


@pytest.mark.slow
@pytest.mark.usefixtures("uses_database", "fake_mongo", "insert_fake_monkey")
def test_cred_special_username_parsing():
    parse_credentials(cred_telem_special_usernames)
    config = ConfigService.get_config(should_decrypt=True)
    assert fake_special_username in dpath.util.get(config, USER_LIST_PATH)


@pytest.mark.slow
@pytest.mark.usefixtures("uses_database", "fake_mongo", "insert_fake_monkey")
def test_cred_telemetry_parsing():
    parse_credentials(cred_telem)
    config = ConfigService.get_config(should_decrypt=True)
    assert fake_username in dpath.util.get(config, USER_LIST_PATH)
    assert fake_nt_hash in dpath.util.get(config, NTLM_HASH_LIST_PATH)
    assert fake_lm_hash in dpath.util.get(config, LM_HASH_LIST_PATH)
    assert fake_password in dpath.util.get(config, PASSWORD_LIST_PATH)


@pytest.mark.slow
@pytest.mark.usefixtures("uses_database", "fake_mongo", "insert_fake_monkey")
def test_cred_storage_in_db():
    parse_credentials(cred_telem)
    cred_docs = list(StolenCredentials.objects())
    assert len(cred_docs) == 1

    stolen_creds = cred_docs[0]
    assert fake_username == stolen_creds.identities[0]["username"]
    assert CredentialComponentType.PASSWORD.name in stolen_creds.secrets
    assert CredentialComponentType.LM_HASH.name in stolen_creds.secrets
    assert CredentialComponentType.NT_HASH.name in stolen_creds.secrets


@pytest.mark.slow
@pytest.mark.usefixtures("uses_database", "fake_mongo", "insert_fake_monkey")
def test_empty_cred_telemetry_parsing():
    default_config = deepcopy(ConfigService.get_config(should_decrypt=True))
    default_usernames = dpath.util.get(default_config, USER_LIST_PATH)
    default_nt_hashes = dpath.util.get(default_config, NTLM_HASH_LIST_PATH)
    default_lm_hashes = dpath.util.get(default_config, LM_HASH_LIST_PATH)
    default_passwords = dpath.util.get(default_config, PASSWORD_LIST_PATH)

    parse_credentials(cred_empty_telem)
    config = ConfigService.get_config(should_decrypt=True)

    assert default_usernames == dpath.util.get(config, USER_LIST_PATH)
    assert default_nt_hashes == dpath.util.get(config, NTLM_HASH_LIST_PATH)
    assert default_lm_hashes == dpath.util.get(config, LM_HASH_LIST_PATH)
    assert default_passwords == dpath.util.get(config, PASSWORD_LIST_PATH)
