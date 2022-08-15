import logging
import time
from typing import Dict, Iterable, Sequence

from common.credentials import Credentials, SSHKeypair, Username
from common.event_queue import IEventQueue
from common.events import CredentialsStolenEvent
from infection_monkey.config import GUID
from infection_monkey.credential_collectors.ssh_collector import ssh_handler
from infection_monkey.i_puppet import ICredentialCollector
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger

logger = logging.getLogger(__name__)

SSH_CREDENTIAL_COLLECTOR_TAG = "SSHCredentialsStolen"


class SSHCredentialCollector(ICredentialCollector):
    """
    SSH keys credential collector
    """

    def __init__(self, telemetry_messenger: ITelemetryMessenger, event_queue: IEventQueue):
        self._telemetry_messenger = telemetry_messenger
        self._event_queue = event_queue

    def collect_credentials(self, _options=None) -> Sequence[Credentials]:
        logger.info("Started scanning for SSH credentials")
        ssh_info = ssh_handler.get_ssh_info(self._telemetry_messenger)
        logger.info("Finished scanning for SSH credentials")
        ssh_collector_credentials = SSHCredentialCollector._to_credentials(ssh_info)

        credentials_stolen_event = SSHCredentialCollector._generate_credentials_stolen_event(
            ssh_collector_credentials
        )
        self._event_queue.publish(credentials_stolen_event)

        return ssh_collector_credentials

    @staticmethod
    def _generate_credentials_stolen_event(
        collected_credentials: Sequence[Credentials],
    ) -> CredentialsStolenEvent:
        credentials_stolen_event = CredentialsStolenEvent(
            source=GUID,
            target=None,
            timestamp=time.time(),
            tags=frozenset({SSH_CREDENTIAL_COLLECTOR_TAG, "T1005", "T1145"}),
            stolen_credentials=collected_credentials,
        )

        return credentials_stolen_event

    @staticmethod
    def _to_credentials(ssh_info: Iterable[Dict]) -> Sequence[Credentials]:
        ssh_credentials = []

        for info in ssh_info:
            identity = None
            secret = None

            if info.get("name", ""):
                identity = Username(info["name"])

            ssh_keypair = {}
            for key in ["public_key", "private_key"]:
                if info.get(key) is not None:
                    ssh_keypair[key] = info[key]

            if len(ssh_keypair):
                secret = SSHKeypair(
                    ssh_keypair.get("private_key", ""), ssh_keypair.get("public_key", "")
                )

            if any([identity, secret]):
                ssh_credentials.append(Credentials(identity, secret))

        return ssh_credentials
