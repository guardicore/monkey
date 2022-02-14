from common.common_consts.post_breach_consts import POST_BREACH_PROCESS_LIST_COLLECTION
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique


class T1082(AttackTechnique):
    tech_id = "T1082"
    relevant_systems = ["Linux", "Windows"]
    unscanned_msg = "Monkey didn't gather any system info on the network."
    scanned_msg = ""
    used_msg = "Monkey gathered system info from machines in the network."
    # TODO: Remove the second item from this list after the TODO in `_run_pba()` in
    #       `automated_master.py` is resolved.
    pba_names = [POST_BREACH_PROCESS_LIST_COLLECTION, "ProcessListCollection"]

    query_for_system_info_collectors = [
        {"$match": {"telem_category": "system_info", "data.network_info": {"$exists": True}}},
        {
            "$project": {
                "machine": {"hostname": "$data.hostname", "ips": "$data.network_info.networks"},
                "aws": "$data.aws",
                "ssh_info": "$data.ssh_info",
                "azure_info": "$data.Azure",
            }
        },
        {
            "$project": {
                "_id": 0,
                "machine": 1,
                "collections": [
                    {
                        "used": {"$and": [{"$gt": ["$aws", {}]}]},
                        "name": {"$literal": "Amazon Web Services info"},
                    },
                    {
                        "used": {
                            "$and": [{"$ifNull": ["$ssh_info", False]}, {"$ne": ["$ssh_info", []]}]
                        },
                        "name": {"$literal": "SSH info"},
                    },
                    {
                        "used": {
                            "$and": [
                                {"$ifNull": ["$azure_info", False]},
                                {"$ne": ["$azure_info", []]},
                            ]
                        },
                        "name": {"$literal": "Azure info"},
                    },
                    {"used": True, "name": {"$literal": "Network interfaces"}},
                ],
            }
        },
        {"$group": {"_id": {"machine": "$machine", "collections": "$collections"}}},
        {"$replaceRoot": {"newRoot": "$_id"}},
    ]

    query_for_pbas = [
        {
            "$match": {
                "$and": [
                    {"telem_category": "post_breach"},
                    {"$or": [{"data.name": pba_name} for pba_name in pba_names]},
                    {"$or": [{"data.os": os} for os in relevant_systems]},
                ]
            }
        },
        {
            "$project": {
                "_id": 0,
                "machine": {
                    "hostname": {"$arrayElemAt": ["$data.hostname", 0]},
                    "ips": [{"$arrayElemAt": ["$data.ip", 0]}],
                },
                "collections": [
                    {
                        "used": {"$arrayElemAt": [{"$arrayElemAt": ["$data.result", 0]}, 1]},
                        "name": {"$literal": "List of running processes"},
                    }
                ],
            }
        },
    ]

    @staticmethod
    def get_report_data():
        def get_technique_status_and_data():
            system_info_data = list(
                mongo.db.telemetry.aggregate(T1082.query_for_system_info_collectors)
            )
            pba_data = list(mongo.db.telemetry.aggregate(T1082.query_for_pbas))
            technique_data = system_info_data + pba_data

            if technique_data:
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, technique_data)

        status, technique_data = get_technique_status_and_data()
        data = {"title": T1082.technique_title()}
        data.update({"technique_data": technique_data})

        data.update(T1082.get_mitigation_by_status(status))
        data.update(T1082.get_message_and_status(status))
        return data
