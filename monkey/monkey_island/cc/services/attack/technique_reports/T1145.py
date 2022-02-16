import logging

from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

logger = logging.getLogger(__name__)


class T1145(AttackTechnique):
    tech_id = "T1145"
    relevant_systems = ["Linux", "Windows"]
    unscanned_msg = "Monkey didn't find any SSH keys."
    scanned_msg = ""
    used_msg = "Monkey found SSH keys on machines in the network."

    # Gets data about ssh keys found
    query = [
        {"$match": {"telem_category": "attack", "data.technique": tech_id}},
        {
            "$lookup": {
                "from": "monkey",
                "localField": "monkey_guid",
                "foreignField": "guid",
                "as": "monkey",
            }
        },
        {
            "$project": {
                "monkey": {"$arrayElemAt": ["$monkey", 0]},
                "status": "$data.status",
                "name": "$data.name",
                "home_dir": "$data.home_dir",
            }
        },
        {
            "$addFields": {
                "_id": 0,
                "machine": {"hostname": "$monkey.hostname", "ips": "$monkey.ip_addresses"},
                "monkey": 0,
            }
        },
        {
            "$group": {
                "_id": {
                    "machine": "$machine",
                    "ssh_info": {"name": "$name", "home_dir": "$home_dir"},
                }
            }
        },
        {"$replaceRoot": {"newRoot": "$_id"}},
    ]

    @staticmethod
    def get_report_data():
        def get_technique_status_and_data():
            ssh_info = list(mongo.db.telemetry.aggregate(T1145.query))
            if ssh_info:
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, ssh_info)

        status, ssh_info = get_technique_status_and_data()

        data = T1145.get_base_data_by_status(status)
        data.update({"ssh_info": ssh_info})
        return data
