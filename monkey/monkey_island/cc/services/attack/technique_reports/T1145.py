from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1145(AttackTechnique):
    tech_id = "T1145"
    unscanned_msg = "Monkey didn't find any shh keys."
    scanned_msg = ""
    used_msg = "Monkey found ssh keys on machines in the network."

    # Gets data about ssh keys found
    query = [{'$match': {'telem_category': 'system_info',
                         'data.ssh_info': {'$elemMatch': {'private_key': {'$exists': True}}}}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname', 'ips': '$data.network_info.networks'},
                           'ssh_info': '$data.ssh_info'}}]

    @staticmethod
    def get_report_data():
        @T1145.is_status_disabled
        def get_technique_status_and_data():
            ssh_info = list(mongo.db.telemetry.aggregate(T1145.query))
            if ssh_info:
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, ssh_info)

        status, ssh_info = get_technique_status_and_data()

        data = T1145.get_base_data_by_status(status)
        data.update({'ssh_info': ssh_info})
        return data
