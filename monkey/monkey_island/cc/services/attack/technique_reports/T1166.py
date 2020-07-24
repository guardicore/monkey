from common.data.post_breach_consts import POST_BREACH_SETUID_SETGID
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "shreyamalviya"


class T1166(AttackTechnique):
    tech_id = "T1166"
    unscanned_msg = "Monkey did not try creating hidden files or folders."
    scanned_msg = "Monkey tried creating hidden files and folders on the system but failed."
    used_msg = "Monkey created hidden files and folders on the system."

    query = [{'$match': {'telem_category': 'post_breach',
                         'data.name': POST_BREACH_SETUID_SETGID}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname',
                                       'ips': '$data.ip'},
                           'result': '$data.result'}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1166.technique_title(), 'info': []}

        setuid_setgid_info = list(mongo.db.telemetry.aggregate(T1166.query))

        status = ScanStatus.UNSCANNED.value
        if setuid_setgid_info:
            successful_PBAs = mongo.db.telemetry.count({'data.name': POST_BREACH_SETUID_SETGID,
                                                        'data.result.1': True})
            status = ScanStatus.USED.value if successful_PBAs else ScanStatus.SCANNED.value

        data.update(T1166.get_base_data_by_status(status))
        data.update({'info': setuid_setgid_info})
        return data
