from copy import deepcopy

import dpath.util
import pytest
from tests.unit_tests.monkey_island.cc.services.telemetry.processing.credentials.conftest import (
    CREDENTIAL_TELEM_TEMPLATE,
)

from common.config_value_paths import SSH_KEYS_PATH, USER_LIST_PATH
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.telemetry.processing.credentials.credentials_parser import (
    parse_credentials,
)

fake_private_key = "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAACmFlczI1N\n"
fake_partial_secret = {"private_key": fake_private_key, "credential_type": "SSH_KEYPAIR"}

fake_username = "ubuntu"
fake_public_key = (
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1u2+50OFRnzOGHpWo69"
    "tc02oMXudeML7pOl7rqXLmdxuj monkey@krk-wpas5"
)
fake_secret_full = {
    "private_key": fake_private_key,
    "public_key": fake_public_key,
    "credential_type": "SSH_KEYPAIR",
}
fake_identity = {"username": fake_username, "credential_type": "USERNAME"}

ssh_telem = deepcopy(CREDENTIAL_TELEM_TEMPLATE)
ssh_telem["data"] = [{"identities": [fake_identity], "secrets": [fake_secret_full]}]


@pytest.mark.slow
@pytest.mark.usefixtures("uses_encryptor", "uses_database", "fake_mongo", "insert_fake_monkey")
def test_ssh_credential_parsing():
    parse_credentials(ssh_telem)
    config = ConfigService.get_config(should_decrypt=True)
    ssh_keypairs = dpath.util.get(config, SSH_KEYS_PATH)
    assert len(ssh_keypairs) == 1
    assert ssh_keypairs[0]["private_key"] == fake_private_key
    assert ssh_keypairs[0]["public_key"] == fake_public_key
    assert fake_username in dpath.util.get(config, USER_LIST_PATH)
