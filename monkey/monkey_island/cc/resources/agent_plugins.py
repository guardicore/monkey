from http import HTTPStatus

from flask import make_response

from monkey_island.cc.resources.AbstractResource import AbstractResource


class AgentPlugins(AbstractResource):
    urls = ["/api/agent-plugins/<string:type>/<string:name>"]

    # Used by monkey. can't secure.
    def get(self, type: str, name: str):
        """
        Gets the plugins of the specified type and name.

        :param type: The type of plugin (e.g. Exploiter)
        :param name: The name of the plugin
        """

        return make_response({}, HTTPStatus.NOT_FOUND)
