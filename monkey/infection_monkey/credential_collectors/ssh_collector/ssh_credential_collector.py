import logging
from typing import Dict, Iterable, Sequence

from infection_monkey.credential_collectors import SSHKeypair, Username
from infection_monkey.credential_collectors.ssh_collector import ssh_handler
from infection_monkey.i_puppet.credential_collection import Credentials, ICredentialCollector
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger

logger = logging.getLogger(__name__)


class SSHCredentialCollector(ICredentialCollector):
    """
    SSH keys credential collector
    """

    def __init__(self, telemetry_messenger: ITelemetryMessenger):
        self._telemetry_messenger = telemetry_messenger

    def collect_credentials(self, _options=None) -> Sequence[Credentials]:
        logger.info("Started scanning for SSH credentials")
        ssh_info = ssh_handler.get_ssh_info(self._telemetry_messenger)
        logger.info("Finished scanning for SSH credentials")

        return SSHCredentialCollector._to_credentials(ssh_info)

    @staticmethod
    def _to_credentials(ssh_info: Iterable[Dict]) -> Sequence[Credentials]:
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
                secrets.append(
                    SSHKeypair(
                        ssh_keypair.get("private_key", ""), ssh_keypair.get("public_key", "")
                    )
                )

            if identities != [] or secrets != []:
                ssh_credentials.append(Credentials(identities, secrets))

        return ssh_credentials
