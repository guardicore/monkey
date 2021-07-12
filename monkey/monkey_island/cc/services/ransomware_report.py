from typing import Dict, List

from monkey_island.cc.services.reporting.report import ReportService


def get_propagation_stats() -> Dict:
    scanned = ReportService.get_scanned()
    exploited = ReportService.get_exploited()

    return {
        "num_scanned_nodes": len(scanned),
        "num_exploited_nodes": len(exploited),
        "count_per_exploit": _get_exploit_counts(exploited),
    }


def _get_exploit_counts(exploited: List[Dict]) -> Dict:
    exploit_counts = {}

    for node in exploited:
        exploits = node["exploits"]
        for exploit in exploits:
            if exploit in exploit_counts:
                exploit_counts[exploit] += 1
            else:
                exploit_counts[exploit] = 1

    return exploit_counts
