import logging
from http import HTTPStatus

from flask import make_response, send_file
from monkeytypes import OperatingSystem

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import RetrievalError

from .. import IAgentBinaryService

logger = logging.getLogger(__name__)


class AgentBinaries(AbstractResource):
    urls = ["/api/agent-binaries/<string:os>"]

    def __init__(self, agent_binary_service: IAgentBinaryService):
        self._agent_binary_service = agent_binary_service

    # Can't be secured, used in manual run commands
    def get(self, os):
        """
        Gets the agent binary for the specified OS

        :param os: Operating systems. Supported OS are: 'linux' and 'windows'
        :return: an agent binary file
        """
        try:
            operating_system = OperatingSystem[os.upper()]
            file = self._agent_binary_service.get_agent_binary(operating_system)

            return send_file(file, mimetype="application/octet-stream")
        except KeyError as err:
            error_msg = f'No Agents are available for unsupported operating system "{os}": {err}'
            logger.error(error_msg)
            return make_response({"error": error_msg}, HTTPStatus.NOT_FOUND)
        except RetrievalError as err:
            logger.error(err)
            return make_response({"error": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR)
