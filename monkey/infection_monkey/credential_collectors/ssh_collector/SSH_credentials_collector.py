import logging
from typing import Dict, Iterable, List

from infection_monkey.credential_collectors import (
    Credentials,
    ICredentialCollector,
    SSHKeypair,
    Username,
)
from infection_monkey.credential_collectors.ssh_collector import ssh_handler

logger = logging.getLogger(__name__)


class SSHCollector(ICredentialCollector):
    """
    SSH keys and known hosts collection module
    """

    def collect_credentials(self, _options=None) -> List[Credentials]:
        logger.info("Started scanning for SSH credentials")
        ssh_info = ssh_handler.get_ssh_info()
        logger.info("Scanned for SSH credentials")

        return SSHCollector._to_credentials(ssh_info)

    @staticmethod
    def _to_credentials(ssh_info: Iterable[Dict]) -> List[Credentials]:
        ssh_credentials = []

        for info in ssh_info:
            credentials_obj = Credentials(identities=[], secrets=[])

            if "name" in info and info["name"] != "":
                credentials_obj.identities.append(Username(info["name"]))

            ssh_keypair = {}
            for key in ["public_key", "private_key", "known_hosts"]:
                if key in info and info.get(key) is not None:
                    ssh_keypair[key] = info[key]

            if len(ssh_keypair):
                credentials_obj.secrets.append(SSHKeypair(ssh_keypair))

            if credentials_obj.identities != [] or credentials_obj.secrets != []:
                ssh_credentials.append(credentials_obj)

        return ssh_credentials
