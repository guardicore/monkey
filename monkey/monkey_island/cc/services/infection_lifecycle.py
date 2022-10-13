import logging

from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.reporting.report import ReportService
from monkey_island.cc.services.reporting.report_generation_synchronisation import (
    is_report_being_generated,
    safe_generate_reports,
)

logger = logging.getLogger(__name__)


def get_completed_steps():
    infection_done = NodeService.is_monkey_finished_running()

    if infection_done:
        _on_finished_infection()
        report_done = ReportService.is_report_generated()
    else:  # Infection is not done
        report_done = False

    return dict(
        run_server=True,
        report_done=report_done,
    )


def _on_finished_infection():
    # Checking is_report_being_generated here, because we don't want to wait to generate a
    # report; rather,
    # we want to skip and reply.
    if not is_report_being_generated() and not ReportService.is_latest_report_exists():
        safe_generate_reports()
