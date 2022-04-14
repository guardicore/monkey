from typing import Mapping

from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.telemetry.processing.credentials import Credentials


class SSHKeyProcessingError(ValueError):
    def __init__(self, msg=""):
        self.msg = f"Error while processing ssh keypair: {msg}"
        super().__init__(self.msg)


def process_ssh_key(keypair: Mapping, credentials: Credentials):
    if len(credentials.identities) != 1:
        raise SSHKeyProcessingError(
            f"SSH credentials have {len(credentials.identities)} users associated with it!"
        )

    if not _contains_both_keys(keypair):
        raise SSHKeyProcessingError("Private or public key missing")

    ConfigService.ssh_add_keys(
        public_key=keypair["public_key"],
        private_key=keypair["private_key"],
    )


def _contains_both_keys(ssh_key: Mapping) -> bool:
    try:
        return ssh_key["public_key"] and ssh_key["private_key"]
    except KeyError:
        return False
