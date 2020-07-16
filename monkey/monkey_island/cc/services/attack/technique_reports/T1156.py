from common.data.post_breach_consts import \
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "shreyamalviya"


class T1156(AttackTechnique):
    tech_id = "T1156"
    unscanned_msg = "Monkey did not try modifying bash startup files on the system."
    scanned_msg = "Monkey tried modifying bash startup files on the system but failed."
    used_msg = "Monkey modified bash startup files on the system."

    query = [{'$match': {'telem_category': 'post_breach',
                         'data.name': POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION,
                         'data.command': {'$regex': 'bash'}}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname',
                                       'ips': ['$data.ip']},
                           'result': '$data.result'}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1156.technique_title(), 'info': []}

        bash_modification_info = list(mongo.db.telemetry.aggregate(T1156.query))

        status = []
        for pba_node in bash_modification_info:
            status.append(pba_node['result'][1])
        status = (ScanStatus.USED.value if any(status) else ScanStatus.SCANNED.value)\
            if status else ScanStatus.UNSCANNED.value

        data.update(T1156.get_base_data_by_status(status))
        data.update({'info': bash_modification_info})
        return data
