from common.data.post_breach_consts import POST_BREACH_TRAP_COMMAND
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "shreyamalviya"


class T1154(AttackTechnique):
    tech_id = "T1154"
    unscanned_msg = "Monkey did not use the trap command."
    scanned_msg = "Monkey tried using the trap command but failed."
    used_msg = "Monkey used the trap command successfully."

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

        status = ScanStatus.UNSCANNED.value
        if trap_command_info:
            successful_PBAs = mongo.db.telemetry.count({'data.name': POST_BREACH_TRAP_COMMAND,
                                                        'data.result.1': True})
            status = ScanStatus.USED.value if successful_PBAs else ScanStatus.SCANNED.value

        data.update(T1154.get_base_data_by_status(status))
        data.update({'info': trap_command_info})
        return data
