from common.common_consts.post_breach_consts import POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1504(PostBreachTechnique):
    tech_id = "T1504"
    relevant_systems = ["Windows"]
    unscanned_msg = "Monkey didn't try modifying PowerShell startup files."
    scanned_msg = "Monkey tried modifying PowerShell startup files but failed."
    used_msg = "Monkey successfully modified PowerShell startup files."
    pba_names = [POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION]

    @staticmethod
    def get_pba_query(*args):
        return [
            {
                "$match": {
                    "telem_category": "post_breach",
                    "data.name": POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "machine": {
                        "hostname": {"$arrayElemAt": ["$data.hostname", 0]},
                        "ips": [{"$arrayElemAt": ["$data.ip", 0]}],
                    },
                    "result": "$data.result",
                }
            },
            {"$unwind": "$result"},
            {"$match": {"result": {"$regex": r"profile\.ps1"}}},
        ]
