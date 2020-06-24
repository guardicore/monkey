from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.database import mongo
from common.utils.attack_utils import ScanStatus
from common.data.post_breach_consts import POST_BREACH_BACKDOOR_USER, POST_BREACH_COMMUNICATE_AS_NEW_USER

__author__ = "shreyamalviya"


class T1136(AttackTechnique):
    tech_id = "T1136"
    unscanned_msg = "Monkey didn't try creating a new user on the network's systems."
    scanned_msg = "Monkey tried creating a new user on the network's systems, but failed."
    used_msg = "Monkey created a new user on the network's systems."

    query = [{'$match': {'telem_category': 'post_breach',
                         '$or': [{'data.name': POST_BREACH_BACKDOOR_USER},
                                 {'data.name': POST_BREACH_COMMUNICATE_AS_NEW_USER}]}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname',
                                       'ips': ['$data.ip']},
                           'result': '$data.result'}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1136.technique_title()}

        create_user_info = list(mongo.db.telemetry.aggregate(T1136.query))

        status = []
        for pba_node in create_user_info:
            status.append(pba_node['result'][1])
        status = (ScanStatus.USED.value if any(status) else ScanStatus.SCANNED.value)\
            if status else ScanStatus.UNSCANNED.value

        data.update(T1136.get_base_data_by_status(status))
        data.update({'info': create_user_info})
        return data
