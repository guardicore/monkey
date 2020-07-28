from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1016(AttackTechnique):
    tech_id = "T1016"
    unscanned_msg = "Monkey didn't gather network configurations."
    scanned_msg = ""
    used_msg = "Monkey gathered network configurations on systems in the network."

    query = [{'$match': {'telem_category': 'system_info', 'data.network_info': {'$exists': True}}},
             {'$project': {'machine': {'hostname': '$data.hostname', 'ips': '$data.network_info.networks'},
                           'networks': '$data.network_info.networks',
                           'netstat': '$data.network_info.netstat'}},
             {'$addFields': {'_id': 0,
                             'netstat': 0,
                             'networks': 0,
                             'info': [
                                 {'used': {'$and': [{'$ifNull': ['$netstat', False]}, {'$gt': ['$netstat', {}]}]},
                                  'name': {'$literal': 'Network connections (netstat)'}},
                                 {'used': {'$and': [{'$ifNull': ['$networks', False]}, {'$gt': ['$networks', {}]}]},
                                  'name': {'$literal': 'Network interface info'}},
                             ]}}]

    @staticmethod
    def get_report_data():
        network_info = []

        if not T1016.is_enabled_in_config():
            status = ScanStatus.DISABLED.value
        else:
            network_info = list(mongo.db.telemetry.aggregate(T1016.query))
            status = ScanStatus.USED.value if network_info else ScanStatus.UNSCANNED.value

        data = T1016.get_base_data_by_status(status)
        data.update({'network_info': network_info})
        return data
