import logging
import os
import platform
import stat
import subprocess
from ipaddress import IPv4Address
from pathlib import Path
from shutil import copyfileobj
from typing import Sequence

from monkeytypes import OTP, OperatingSystem

from common.common_consts import AGENT_OTP_ENVIRONMENT_VARIABLE
from monkey_island.cc.repositories import RetrievalError
from monkey_island.cc.services import IAgentBinaryService

logger = logging.getLogger(__name__)

AGENT_NAMES = {
    OperatingSystem.LINUX: "monkey-linux-64",
    OperatingSystem.WINDOWS: "monkey-windows-64.exe",
}


class LocalMonkeyRunService:
    def __init__(
        self,
        data_dir: Path,
        agent_binary_service: IAgentBinaryService,
        island_ip_addresses: Sequence[IPv4Address],
        island_port: int,
    ):
        self._data_dir = data_dir
        self._agent_binary_service = agent_binary_service
        self._ips = island_ip_addresses
        self._island_port = island_port

    def run_local_monkey(self, otp: OTP):
        # get the monkey executable suitable to run on the server
        try:
            operating_system = OperatingSystem[platform.system().upper()]
            agent_binary = self._agent_binary_service.get_agent_binary(operating_system)
        except RetrievalError as err:
            logger.error(
                f"No Agent can be retrieved for the specified operating system"
                f'"{operating_system}"'
            )
            return False, str(err)
        except KeyError as err:
            logger.error(
                f"No Agents are available for unsupported operating system" f'"{operating_system}"'
            )
            return False, str(err)
        except Exception as err:
            logger.error(f"Error running agent from island: {err}")
            return False, str(err)

        dest_path = self._data_dir / AGENT_NAMES[operating_system]

        # copy the executable to temp path (don't run the monkey from its current location as it may
        # delete itself)
        try:
            with open(dest_path, "wb") as dest_agent:
                copyfileobj(agent_binary, dest_agent)

            dest_path.chmod(stat.S_IRWXU | stat.S_IRWXG)
        except Exception as exc:
            logger.error("Copy file failed", exc_info=True)
            return False, "Copy file failed: %s" % exc

        # run the monkey
        try:
            ip = self._ips[0]
            port = self._island_port

            process_env = os.environ.copy()
            process_env[AGENT_OTP_ENVIRONMENT_VARIABLE] = otp.get_secret_value()
            args = [str(dest_path), "m0nk3y", "-s", f"{ip}:{port}"]
            subprocess.Popen(args, cwd=self._data_dir, env=process_env)
        except Exception as exc:
            logger.error("popen failed", exc_info=True)
            return False, "popen failed: %s" % exc

        return True, ""
