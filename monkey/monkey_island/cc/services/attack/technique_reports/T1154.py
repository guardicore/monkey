from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.database import mongo
from common.utils.attack_utils import ScanStatus
from common.data.post_breach_consts import POST_BREACH_TRAP_COMMAND


__author__ = "shreyamalviya"


class T1154(AttackTechnique):
    tech_id = "T1154"
    unscanned_msg = "Monkey did not use the trap command on the system."
    scanned_msg = "Monkey tried using the trap command but failed on the system."
    used_msg = "Monkey used the trap command on the system."

    query = [{'$match': {'telem_category': 'post_breach',
                         'data.name': POST_BREACH_TRAP_COMMAND}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname',
                                       'ips': ['$data.ip']},
                           'result': '$data.result'}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1154.technique_title(), 'info': []}

        trap_command_info = list(mongo.db.telemetry.aggregate(T1154.query))

        status = []
        for pba_node in trap_command_info:
            status.append(pba_node['result'][1])
        status = (ScanStatus.USED.value if any(status) else ScanStatus.SCANNED.value)\
            if status else ScanStatus.UNSCANNED.value

        data.update(T1154.get_base_data_by_status(status))
        data.update({'info': trap_command_info})
        return data
