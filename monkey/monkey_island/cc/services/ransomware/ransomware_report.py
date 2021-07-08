from monkey_island.cc.database import mongo
from typing import Dict, List

from monkey_island.cc.services.reporting.report import ReportService


class RansomwareReportService:
    @staticmethod
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
            {
                "$lookup": {
                    "from": "edge",
                    "localField": "monkey._id",
                    "foreignField": "dst_node_id",
                    "as": "edge",
                }
            },
            {
                "$project": {
                    "monkey": "$monkey",
                    "files_encrypted": "$files_encrypted",
                    "edge": {"$arrayElemAt": ["$edge", 0]},
                }
            },
            {
                "$project": {
                    "hostname": "$monkey.hostname",
                    "successful_exploits": {
                        "$filter": {
                            "input": "$edge.exploits",
                            "as": "exploit",
                            "cond": {"$eq": ["$$exploit.result", True]},
                        }
                    },
                    "files_encrypted": "$files_encrypted",
                }
            },
            {
                "$addFields": {
                    "successful_exploit": {"$arrayElemAt": ["$successful_exploits", 0]},
                }
            },
            {
                "$project": {
                    "hostname": "$hostname",
                    "exploiter": "$successful_exploit.info.display_name",
                    "files_encrypted": "$files_encrypted",
                }
            },
        ]

        table_data = list(mongo.db.telemetry.aggregate(query))
        for encryption_entry in table_data:
            if "exploiter" not in encryption_entry:
                encryption_entry["exploiter"] = "Manual run"
        return table_data

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
