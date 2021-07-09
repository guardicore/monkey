from monkey_island.cc.database import mongo
from monkey_island.cc.services.reporting.report import ReportService
from typing import Dict, List

from monkey_island.cc.services.reporting.report import ReportService


def get_encrypted_files_table():
    query = [
        {"$match": {"telem_category": "file_encryption"}},
        {"$unwind": "$data.files"},
        {
            "$group": {
                "_id": {"monkey_guid": "$monkey_guid", "files_encrypted": "$data.files.success"}
            }
        },
        {"$replaceRoot": {"newRoot": "$_id"}},
        {"$sort": {"files_encrypted": -1}},
        {
            "$group": {
                "_id": {"monkey_guid": "$monkey_guid"},
                "monkey_guid": {"$first": "$monkey_guid"},
                "files_encrypted": {"$first": "$files_encrypted"},
            }
        },
        {
            "$lookup": {
                "from": "monkey",
                "localField": "_id.monkey_guid",
                "foreignField": "guid",
                "as": "monkey",
            }
        },
        {
            "$project": {
                "monkey": {"$arrayElemAt": ["$monkey", 0]},
                "files_encrypted": "$files_encrypted",
            }
        },
    ]

    monkeys = list(mongo.db.telemetry.aggregate(query))
    exploited_nodes = ReportService.get_exploited()
    for monkey in monkeys:
        monkey["exploits"] = _get_monkey_origin_exploits(
            monkey["monkey"]["hostname"], exploited_nodes
        )
        monkey["hostname"] = monkey["monkey"]["hostname"]
        del monkey["monkey"]
        del monkey["_id"]
    return monkeys


def _get_monkey_origin_exploits(monkey_hostname, exploited_nodes):
    origin_exploits = [
        exploited_node["exploits"]
        for exploited_node in exploited_nodes
        if exploited_node["label"] == monkey_hostname
    ]
    if origin_exploits:
        return origin_exploits[0]
    else:
        return ["Manual execution"]

def get_propagation_stats() -> Dict:
    scanned = ReportService.get_scanned()
    exploited = ReportService.get_exploited()

    return {
        "num_scanned_nodes": len(scanned),
        "num_exploited_nodes": len(exploited),
        "num_exploited_per_exploit": _get_exploit_counts(exploited),
    }


def _get_exploit_counts(exploited: List[Dict]) -> Dict:
    exploit_counts = {}

    for node in exploited:
        for exploit in node["exploits"]:
            exploit_counts[exploit] = exploit_counts.get(exploit, 0) + 1

    return exploit_counts
