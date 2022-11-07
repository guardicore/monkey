import logging

from monkey_island.cc.repository import IAgentRepository
from monkey_island.cc.services.reporting.report import ReportService
from monkey_island.cc.services.reporting.report_generation_synchronisation import (
    is_report_being_generated,
    safe_generate_reports,
)

logger = logging.getLogger(__name__)


def is_report_done(agent_repository: IAgentRepository) -> bool:
    infection_done = _is_infection_done(agent_repository)

    if infection_done:
        _on_finished_infection()
        report_done = ReportService.is_report_generated()
    else:  # Infection is not done
        report_done = False

    return report_done


def _is_infection_done(agent_repository: IAgentRepository) -> bool:
    any_agent_exists = bool(agent_repository.get_agents())
    any_agent_running = bool(agent_repository.get_running_agents())
    return any_agent_exists and not any_agent_running


def _on_finished_infection():
    # Checking is_report_being_generated here, because we don't want to wait to generate a
    # report; rather,
    # we want to skip and reply.
    if not is_report_being_generated() and ReportService.report_is_outdated():
        safe_generate_reports()
