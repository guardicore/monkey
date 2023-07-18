from flask import jsonify
from flask_security import auth_token_required, roles_accepted

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import IAgentEventRepository, IMachineRepository
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService
from monkey_island.cc.services.authentication_service import AccountRole
from monkey_island.cc.services.ransomware import ransomware_report


class RansomwareReport(AbstractResource):
    urls = ["/api/report/ransomware"]

    def __init__(
        self,
        event_repository: IAgentEventRepository,
        machine_repository: IMachineRepository,
        agent_plugin_service: IAgentPluginService,
    ):
        self._event_repository = event_repository
        self._machine_repository = machine_repository
        self._agent_plugin_service = agent_plugin_service

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        return jsonify(
            {
                "propagation_stats": ransomware_report.get_propagation_stats(
                    self._event_repository, self._machine_repository, self._agent_plugin_service
                ),
            }
        )
