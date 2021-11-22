from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique


class T1016(AttackTechnique):
    tech_id = "T1016"
    relevant_systems = ["Linux", "Windows"]
    unscanned_msg = "Monkey didn't gather network configurations."
    scanned_msg = ""
    used_msg = "Monkey gathered network configurations on systems in the network."

    query = [
        {"$match": {"telem_category": "system_info", "data.network_info": {"$exists": True}}},
        {
            "$project": {
                "machine": {"hostname": "$data.hostname", "ips": "$data.network_info.networks"},
                "networks": "$data.network_info.networks",
            }
        },
        {
            "$addFields": {
                "_id": 0,
                "networks": 0,
                "info": [
                    {
                        "used": {
                            "$and": [{"$ifNull": ["$networks", False]}, {"$gt": ["$networks", {}]}]
                        },
                        "name": {"$literal": "Network interface info"},
                    },
                ],
            }
        },
    ]

    @staticmethod
    def get_report_data():
        def get_technique_status_and_data():
            network_info = list(mongo.db.telemetry.aggregate(T1016.query))
            status = ScanStatus.USED.value if network_info else ScanStatus.UNSCANNED.value
            return (status, network_info)

        status, network_info = get_technique_status_and_data()

        data = T1016.get_base_data_by_status(status)
        data.update({"network_info": network_info})
        return data
