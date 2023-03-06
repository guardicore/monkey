from flask import jsonify
from flask_security import auth_token_required

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import IAgentRepository
from monkey_island.cc.services.infection_lifecycle import is_report_done


class ReportGenerationStatus(AbstractResource):
    urls = ["/api/report-generation-status"]

    def __init__(self, agent_repository: IAgentRepository):
        self._agent_repository = agent_repository

    def get(self):
        return self.report_generation_status()

    @auth_token_required
    def report_generation_status(self):
        return jsonify(
            report_done=is_report_done(self._agent_repository),
        )
