from common.data.post_breach_consts import POST_BREACH_HIDDEN_FILES
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "shreyamalviya"


class T1158(AttackTechnique):
    tech_id = "T1158"
    unscanned_msg = "Monkey did not try creating hidden files or folders."
    scanned_msg = "Monkey tried creating hidden files and folders on the system but failed."
    used_msg = "Monkey created hidden files and folders on the system."

    query = [{'$match': {'telem_category': 'post_breach',
                         'data.name': POST_BREACH_HIDDEN_FILES}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname',
                                       'ips': '$data.ip'},
                           'result': '$data.result'}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1158.technique_title(), 'info': []}

        hidden_file_info = list(mongo.db.telemetry.aggregate(T1158.query))

        status = ScanStatus.UNSCANNED.value
        if hidden_file_info:
            successful_PBAs = mongo.db.telemetry.count({'data.name': POST_BREACH_HIDDEN_FILES,
                                                        'data.result.1': True})
            status = ScanStatus.USED.value if successful_PBAs else ScanStatus.SCANNED.value

        data.update(T1158.get_base_data_by_status(status))
        data.update({'info': hidden_file_info})
        return data
