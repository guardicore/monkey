import logging
from pathlib import Path

from flask import make_response, send_from_directory

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH

logger = logging.getLogger(__name__)

AGENTS = {
    "linux": "monkey-linux-64",
    "windows": "monkey-windows-64.exe",
}


class UnsupportedOSError(Exception):
    pass


class AgentBinaries(AbstractResource):
    urls = ["/api/agent-binaries/<string:os>"]

    # Used by monkey. can't secure.
    def get(self, os):
        try:
            path = get_agent_executable_path(os)
            return send_from_directory(path.parent, path.name)
        except UnsupportedOSError as ex:
            logger.error(ex)
            return make_response({"error": str(ex)}, 404)


def get_agent_executable_path(os: str) -> Path:
    try:
        agent_path = get_executable_full_path(AGENTS[os])
        logger.debug(f'Local path for {os} executable is "{agent_path}"')
        if not agent_path.is_file():
            logger.error(f"File {agent_path} not found")

        return agent_path
    except KeyError:
        logger.warning(f"No monkey executables could be found for the host os: {os}")
        raise UnsupportedOSError(f'No Agents are available for unsupported operating system "{os}"')


def get_executable_full_path(executable_filename: str) -> Path:
    return Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "binaries" / executable_filename
