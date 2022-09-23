import logging

from monkey_island.cc.models import Monkey
from monkey_island.cc.models.agent_controls import AgentControls
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.reporting.report import ReportService
from monkey_island.cc.services.reporting.report_generation_synchronisation import (
    is_report_being_generated,
    safe_generate_reports,
)

logger = logging.getLogger(__name__)


def should_agent_die(guid: int) -> bool:
    monkey = Monkey.objects(guid=str(guid)).first()
    return _should_agent_stop(monkey) or _is_monkey_killed_manually(monkey)


def _should_agent_stop(monkey: Monkey) -> bool:
    if monkey.should_stop:
        # Only stop the agent once, to allow further runs on that machine
        monkey.should_stop = False
        monkey.save()
        return True
    return False


def _is_monkey_killed_manually(monkey: Monkey) -> bool:
    terminate_timestamp = AgentControls.objects.first().last_stop_all
    if terminate_timestamp is None:
        return False
    if monkey.has_parent():
        launch_timestamp = monkey.get_parent().launch_time
    else:
        launch_timestamp = monkey.launch_time
    return int(terminate_timestamp) >= int(launch_timestamp)


def get_completed_steps():
    is_any_exists = NodeService.is_any_monkey_exists()
    infection_done = NodeService.is_monkey_finished_running()

    if infection_done:
        _on_finished_infection()
        report_done = ReportService.is_report_generated()
    else:  # Infection is not done
        report_done = False

    return dict(
        run_server=True,
        run_monkey=is_any_exists,
        infection_done=infection_done,
        report_done=report_done,
    )


def _on_finished_infection():
    # Checking is_report_being_generated here, because we don't want to wait to generate a
    # report; rather,
    # we want to skip and reply.
    if not is_report_being_generated() and not ReportService.is_latest_report_exists():
        safe_generate_reports()
