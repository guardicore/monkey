import logging
from typing import Dict, Iterable, List

from infection_monkey.credential_collectors import SSHKeypair, Username
from infection_monkey.credential_collectors.ssh_collector import ssh_handler
from infection_monkey.i_puppet.credential_collection import Credentials, ICredentialCollector

logger = logging.getLogger(__name__)


class SSHCredentialCollector(ICredentialCollector):
    """
    SSH keys credential collector
    """

    def collect_credentials(self, _options=None) -> List[Credentials]:
        logger.info("Started scanning for SSH credentials")
        ssh_info = ssh_handler.get_ssh_info()
        logger.info("Finished scanning for SSH credentials")

        return SSHCredentialCollector._to_credentials(ssh_info)

    @staticmethod
    def _to_credentials(ssh_info: Iterable[Dict]) -> List[Credentials]:
        ssh_credentials = []

        for info in ssh_info:
            identities = []
            secrets = []

            if info.get("name", ""):
                identities.append(Username(info["name"]))

            ssh_keypair = {}
            for key in ["public_key", "private_key"]:
                if info.get(key) is not None:
                    ssh_keypair[key] = info[key]

            if len(ssh_keypair):
                secrets.append(SSHKeypair(ssh_keypair))

            if identities != [] or secrets != []:
                ssh_credentials.append(Credentials(identities, secrets))

        return ssh_credentials
