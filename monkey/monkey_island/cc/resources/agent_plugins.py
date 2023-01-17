import logging
from http import HTTPStatus

from flask import make_response

from common import OperatingSystem
from common.agent_plugins import AgentPluginType
from monkey_island.cc.repositories import IAgentPluginRepository, UnknownRecordError
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class AgentPlugins(AbstractResource):
    urls = ["/api/agent-plugins/<string:host_os>/<string:plugin_type>/<string:name>"]

    def __init__(self, agent_plugin_repository: IAgentPluginRepository):
        self._agent_plugin_repository = agent_plugin_repository

    # Used by monkey. can't secure.
    def get(self, host_os: str, plugin_type: str, name: str):
        """
        Get the plugin of the specified operating system, type and name.

        :param host_os: The operating system on which the plugin should run
        :param type: The type of plugin (e.g. Exploiter)
        :param name: The name of the plugin
        """
        try:
            host_operating_system = OperatingSystem(host_os)
        except ValueError:
            message = f"Invalid os: '{host_os}'."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)

        try:
            agent_plugin_type = AgentPluginType(plugin_type)
        except ValueError:
            message = f"Invalid type '{plugin_type}'."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)

        try:
            agent_plugin = self._agent_plugin_repository.get_plugin(
                host_operating_system=host_operating_system,
                plugin_type=agent_plugin_type,
                name=name,
            )
            return make_response(agent_plugin.dict(simplify=True), HTTPStatus.OK)
        except UnknownRecordError:
            message = f"Plugin '{name}' of type '{plugin_type}' not found for os '{host_os}'."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)
