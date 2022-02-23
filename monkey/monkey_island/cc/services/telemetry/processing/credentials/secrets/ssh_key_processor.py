from typing import Mapping

from monkey_island.cc.models import Monkey
from monkey_island.cc.server_utils.encryption import get_datastore_encryptor
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.telemetry.processing.credentials import Credentials


class SSHKeyProcessingError(ValueError):
    def __init__(self, msg=""):
        self.msg = f"Error while processing ssh keypair: {msg}"
        super().__init__(self.msg)


def process_ssh_key(keypair: Mapping, credentials: Credentials):
    if len(credentials.identities) != 1:
        raise SSHKeyProcessingError(
            f"SSH credentials have {len(credentials.identities)}" f" users associated with " f"it!"
        )

    if not _contains_both_keys(keypair):
        raise SSHKeyProcessingError("Private or public key missing!")

    # TODO SSH key should be associated with IP that monkey exploited
    ip = Monkey.get_single_monkey_by_guid(credentials.monkey_guid).ip_addresses[0]
    username = credentials.identities[0]["username"]

    encrypted_keys = _encrypt_ssh_keys(keypair)

    ConfigService.ssh_add_keys(
        user=username,
        public_key=encrypted_keys["public_key"],
        private_key=encrypted_keys["private_key"],
        ip=ip,
    )


def _contains_both_keys(ssh_key: Mapping) -> bool:
    try:
        return ssh_key["public_key"] and ssh_key["private_key"]
    except KeyError:
        return False


def _encrypt_ssh_keys(ssh_key: Mapping) -> Mapping:
    encrypted_keys = {}
    for field in ["public_key", "private_key"]:
        encrypted_keys[field] = get_datastore_encryptor().encrypt(ssh_key[field])
    return encrypted_keys
