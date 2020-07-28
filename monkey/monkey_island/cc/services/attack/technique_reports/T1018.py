from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1018(AttackTechnique):
    tech_id = "T1018"
    unscanned_msg = "Monkey didn't find any machines on the network."
    scanned_msg = ""
    used_msg = "Monkey found machines on the network."

    query = [{'$match': {'telem_category': 'scan'}},
             {'$sort': {'timestamp': 1}},
             {'$group': {'_id': {'monkey_guid': '$monkey_guid'},
                         'machines': {'$addToSet': '$data.machine'},
                         'started': {'$first': '$timestamp'},
                         'finished': {'$last': '$timestamp'}}},
             {'$lookup': {'from': 'monkey',
                          'localField': '_id.monkey_guid',
                          'foreignField': 'guid',
                          'as': 'monkey_tmp'}},
             {'$addFields': {'_id': 0, 'monkey_tmp': {'$arrayElemAt': ['$monkey_tmp', 0]}}},
             {'$addFields': {'monkey': {'hostname': '$monkey_tmp.hostname',
                                        'ips': '$monkey_tmp.ip_addresses'},
                             'monkey_tmp': 0}}]

    @staticmethod
    def get_report_data():
        @T1018.is_status_disabled
        def get_technique_status_and_data():
            scan_info = list(mongo.db.telemetry.aggregate(T1018.query))
            if scan_info:
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, scan_info)

        status, scan_info = get_technique_status_and_data()

        data = T1018.get_base_data_by_status(status)
        data.update({'scan_info': scan_info})
        return data
