from common.common_consts.credentials_type import CredentialComponentType
from monkey_island.cc.models import Monkey
from monkey_island.cc.server_utils.encryption import get_datastore_encryptor
from monkey_island.cc.services.config import ConfigService


class SSHKeyProcessingError(ValueError):
    def __init__(self, msg=""):
        self.msg = f"Error while processing ssh keypair: {msg}"
        super().__init__(self.msg)


def process_ssh_key(credentials: dict, monkey_guid: str):
    if len(credentials["identities"]) != 1:
        raise SSHKeyProcessingError(
            f'SSH credentials have {len(credentials["identities"])}' f" users associated with it!"
        )

    for ssh_key in credentials["secrets"]:
        if not ssh_key["credential_type"] == CredentialComponentType.SSH_KEYPAIR.value:
            raise SSHKeyProcessingError("SSH credentials contain secrets that are not keypairs")

        if not ssh_key["public_key"] or not ssh_key["private_key"]:
            raise SSHKeyProcessingError("Private or public key missing!")

        # TODO SSH key should be associated with IP that monkey exploited
        ip = Monkey.get_single_monkey_by_guid(monkey_guid).ip_addresses[0]
        username = credentials["identities"][0]["username"]

        encrypt_system_info_ssh_keys(ssh_key)

        ConfigService.ssh_add_keys(
            user=username,
            public_key=ssh_key["public_key"],
            private_key=ssh_key["private_key"],
            ip=ip,
        )


def encrypt_system_info_ssh_keys(ssh_key: dict):
    for field in ["public_key", "private_key"]:
        ssh_key[field] = get_datastore_encryptor().encrypt(ssh_key[field])
