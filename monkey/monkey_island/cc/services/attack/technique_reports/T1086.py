from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique


class T1086(AttackTechnique):
    tech_id = "T1086"
    relevant_systems = ["Windows"]
    unscanned_msg = "Monkey didn't run PowerShell."
    scanned_msg = ""
    used_msg = "Monkey successfully ran PowerShell commands on exploited machines in the network."

    query_for_exploits = [
        {
            "$match": {
                "telem_category": "exploit",
                "data.info.executed_cmds": {"$elemMatch": {"powershell": True}},
            }
        },
        {"$project": {"telem_category": 1, "machine": "$data.machine", "info": "$data.info"}},
        {
            "$project": {
                "_id": 0,
                "telem_category": 1,
                "machine": 1,
                "info.finished": 1,
                "info.executed_cmds": {
                    "$filter": {
                        "input": "$info.executed_cmds",
                        "as": "command",
                        "cond": {"$eq": ["$$command.powershell", True]},
                    }
                },
            }
        },
        {"$group": {"_id": "$machine", "data": {"$push": "$$ROOT"}}},
    ]

    query_for_pbas = [
        {
            "$match": {
                "telem_category": "post_breach",
                "$or": [
                    {"data.command": {"$regex": r"\.ps1"}},
                    {"data.command": {"$regex": "powershell"}},
                    {"data.result": {"$regex": r"\.ps1"}},
                ],
            },
        },
        {
            "$project": {
                "_id": 0,
                "telem_category": 1,
                "machine.hostname": "$data.hostname",
                "machine.ips": [{"$arrayElemAt": ["$data.ip", 0]}],
                "info": "$data.result",
            }
        },
    ]

    @staticmethod
    def get_report_data():
        def get_technique_status_and_data():
            exploit_cmd_data = list(mongo.db.telemetry.aggregate(T1086.query_for_exploits))
            pba_cmd_data = list(mongo.db.telemetry.aggregate(T1086.query_for_pbas))
            cmd_data = exploit_cmd_data + pba_cmd_data

            if cmd_data:
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, cmd_data)

        status, cmd_data = get_technique_status_and_data()
        data = {"title": T1086.technique_title(), "cmds": cmd_data}

        data.update(T1086.get_message_and_status(status))
        return data
