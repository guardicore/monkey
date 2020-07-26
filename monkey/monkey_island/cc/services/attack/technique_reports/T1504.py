from common.data.post_breach_consts import \
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "shreyamalviya"


class T1504(AttackTechnique):
    tech_id = "T1504"
    unscanned_msg = "Monkey did not try modifying powershell startup files on the system."
    scanned_msg = "Monkey tried modifying powershell startup files on the system but failed."
    used_msg = "Monkey modified powershell startup files on the system."

    query = [{'$match': {'telem_category': 'post_breach',
                         'data.name': POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': {'$arrayElemAt': ['$data.hostname', 0]},
                                       'ips': [{'$arrayElemAt': ['$data.ip', 0]}]},
                           'result': '$data.result'}},
             {'$unwind': '$result'},
             {'$match': {'result': {'$regex': r'profile\.ps1'}}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1504.technique_title(), 'info': []}

        powershell_startup_modification_info = list(mongo.db.telemetry.aggregate(T1504.query))

        status = ScanStatus.UNSCANNED.value
        if powershell_startup_modification_info:
            successful_PBAs = mongo.db.telemetry.count({'data.name': POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION,
                                                        'data.result.1': True})
            status = ScanStatus.USED.value if successful_PBAs else ScanStatus.SCANNED.value

        data.update(T1504.get_base_data_by_status(status))
        data.update({'info': powershell_startup_modification_info})
        return data
