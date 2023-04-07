import logging
from http import HTTPStatus

from flask import make_response, send_file

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import IAgentBinaryRepository, RetrievalError

logger = logging.getLogger(__name__)


class AgentBinaries(AbstractResource):
    urls = ["/api/agent-binaries/<string:os>"]

    def __init__(self, agent_binary_repository: IAgentBinaryRepository):
        self._agent_binary_repository = agent_binary_repository

    # Can't be secured, used in manual run commands
    def get(self, os):
        """
        Gets the agent binary for the specified OS

        :param os: Operating systems. Supported OS are: 'linux' and 'windows'
        :return: an agent binary file
        """
        try:
            agent_binaries = {
                "linux": self._agent_binary_repository.get_linux_binary,
                "windows": self._agent_binary_repository.get_windows_binary,
            }

            file = agent_binaries[os]()

            return send_file(file, mimetype="application/octet-stream")
        except KeyError as err:
            error_msg = f'No Agents are available for unsupported operating system "{os}": {err}'
            logger.error(error_msg)
            return make_response({"error": error_msg}, HTTPStatus.NOT_FOUND)
        except RetrievalError as err:
            logger.error(err)
            return make_response({"error": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR)
