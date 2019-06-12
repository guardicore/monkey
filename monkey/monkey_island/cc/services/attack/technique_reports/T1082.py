from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1082(AttackTechnique):

    tech_id = "T1082"
    unscanned_msg = "Monkey didn't gather any system info on the network."
    scanned_msg = ""
    used_msg = "Monkey gathered system info from machines in the network."

    # Gets data about successful PTH logins
    query = [{'$match': {'telem_type': 'system_info_collection'},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname', 'ips': '$data.network_info.networks'},
                           'info': {'aws': '$data.aws',
                                    'process_list': '$data.process_list.1'
                           'attempt_cnt': {'$size': '$data.attempts'},
                           'attempts': {'$filter': {'input': '$data.attempts',
                                                    'as': 'attempt',
                                                    'cond': {'$eq': ['$$attempt.result', True]}}}}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1082.technique_title(T1082.tech_id)}
        successful_logins = list(mongo.db.telemetry.aggregate(T1082.query))
        data.update({'successful_logins': successful_logins})
        if successful_logins:
            data.update({'message': T1082.used_msg, 'status': ScanStatus.USED.name})
        elif mongo.db.telemetry.count_documents(T1082.login_attempt_query):
            data.update({'message': T1082.scanned_msg, 'status': ScanStatus.SCANNED.name})
        else:
            data.update({'message': T1082.unscanned_msg, 'status': ScanStatus.UNSCANNED.name})
        return data
