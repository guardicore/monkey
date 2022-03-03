import hashlib
import logging
from pathlib import Path

import flask_restful
from flask import make_response, send_from_directory

from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH

logger = logging.getLogger(__name__)

AGENTS = {
    "linux": "monkey-linux-64",
    "windows": "monkey-windows-64.exe",
}


class UnsupportedOSError(Exception):
    pass


class MonkeyDownload(flask_restful.Resource):

    # Used by monkey. can't secure.
    def get(self, host_os):
        try:
            path = get_agent_executable_path(host_os)
            return send_from_directory(path.parent, path.name)
        except UnsupportedOSError as ex:
            logger.error(ex)
            return make_response({"error": str(ex)}, 404)

    @staticmethod
    def log_executable_hashes():
        """
        Logs all the hashes of the monkey executables for debugging ease (can check what Monkey
        version you have etc.).
        """
        filenames = set(AGENTS.values())
        for filename in filenames:
            filepath = get_executable_full_path(filename)
            if filepath.is_file():
                with open(filepath, "rb") as monkey_exec_file:
                    file_contents = monkey_exec_file.read()
                    file_sha256_hash = hashlib.sha256(file_contents).hexdigest()
                    logger.debug(f"{filename} SHA-256 hash: {file_sha256_hash}")
            else:
                logger.debug(f"No monkey executable for {filepath}")


def get_agent_executable_path(host_os: str) -> Path:
    try:
        agent_path = get_executable_full_path(AGENTS[host_os])
        logger.debug(f'Local path for {host_os} executable is "{agent_path}"')
        if not agent_path.is_file():
            logger.error(f"File {agent_path} not found")

        return agent_path
    except KeyError:
        logger.warning(f"No monkey executables could be found for the host os: {host_os}")
        raise UnsupportedOSError(
            f'No Agents are available for unsupported operating system "{host_os}"'
        )


def get_executable_full_path(executable_filename: str) -> Path:
    return Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "binaries" / executable_filename
