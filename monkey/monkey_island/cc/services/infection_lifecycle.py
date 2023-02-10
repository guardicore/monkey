import logging

from monkey_island.cc.repositories import IAgentRepository
from monkey_island.cc.services.reporting.report import ReportService

logger = logging.getLogger(__name__)


def is_report_done(agent_repository: IAgentRepository) -> bool:
    infection_done = _is_infection_done(agent_repository)

    if infection_done:
        ReportService.update_report()
        report_done = ReportService.is_report_generated()
    else:  # Infection is not done
        report_done = False

    return report_done


def _is_infection_done(agent_repository: IAgentRepository) -> bool:
    any_agent_exists = bool(agent_repository.get_agents())
    any_agent_running = bool(agent_repository.get_running_agents())
    return any_agent_exists and not any_agent_running
