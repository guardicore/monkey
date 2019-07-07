from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1082(AttackTechnique):

    tech_id = "T1082"
    unscanned_msg = "Monkey didn't gather any system info on the network."
    scanned_msg = ""
    used_msg = "Monkey gathered system info from machines in the network."

    query = [{'$match': {'telem_category': 'system_info_collection'}},
             {'$project': {'machine': {'hostname': '$data.hostname', 'ips': '$data.network_info.networks'},
                           'aws': '$data.aws',
                           'netstat': '$data.network_info.netstat',
                           'process_list': '$data.process_list',
                           'ssh_info': '$data.ssh_info',
                           'azure_info': '$data.Azure'}},
             {'$project': {'_id': 0,
                           'machine': 1,
                           'collections': [
                             {'used': {'$and': [{'$ifNull': ['$netstat', False]}, {'$gt': ['$aws', {}]}]},
                              'name': {'$literal': 'Amazon Web Services info'}},
                             {'used': {'$and': [{'$ifNull': ['$process_list', False]}, {'$gt': ['$process_list', {}]}]},
                              'name': {'$literal': 'Running process list'}},
                             {'used': {'$and': [{'$ifNull': ['$netstat', False]}, {'$ne': ['$netstat', []]}]},
                              'name': {'$literal': 'Network connections'}},
                             {'used': {'$and': [{'$ifNull': ['$ssh_info', False]}, {'$ne': ['$ssh_info', []]}]},
                              'name': {'$literal': 'SSH info'}},
                             {'used': {'$and': [{'$ifNull': ['$azure_info', False]}, {'$ne': ['$azure_info', []]}]},
                              'name': {'$literal': 'Azure info'}}
                             ]}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1082.technique_title()}
        system_info = list(mongo.db.telemetry.aggregate(T1082.query))
        data.update({'system_info': system_info})
        if system_info:
            status = ScanStatus.USED
        else:
            status = ScanStatus.UNSCANNED
        data.update(T1082.get_message_and_status(status))
        return data
