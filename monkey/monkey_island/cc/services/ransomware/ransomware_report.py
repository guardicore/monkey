from typing import Dict, List

from monkey_island.cc.repositories import IAgentEventRepository, IMachineRepository
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService
from monkey_island.cc.services.reporting.exploitations.monkey_exploitation import (
    MonkeyExploitation,
    get_monkey_exploited,
)
from monkey_island.cc.services.reporting.report import ReportService


def get_propagation_stats(
    event_repository: IAgentEventRepository,
    machine_repository: IMachineRepository,
    agent_plugin_service: IAgentPluginService,
) -> Dict:
    scanned = ReportService.get_scanned()
    exploited = get_monkey_exploited(event_repository, machine_repository, agent_plugin_service)

    return {
        "num_scanned_nodes": len(scanned),
        "num_exploited_nodes": len(exploited),
        "num_exploited_per_exploit": _get_exploit_counts(exploited),
    }


def _get_exploit_counts(exploited: List[MonkeyExploitation]) -> Dict[str, int]:
    exploit_counts: Dict[str, int] = {}

    for node in exploited:
        for exploit in node.exploits:
            exploit_counts[exploit] = exploit_counts.get(exploit, 0) + 1

    return exploit_counts
