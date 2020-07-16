from common.data.post_breach_consts import POST_BREACH_JOB_SCHEDULING
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "shreyamalviya"


class T1053(AttackTechnique):
    tech_id = "T1053"
    unscanned_msg = "Monkey did not try scheduling a job on Windows."
    scanned_msg = "Monkey tried scheduling a job on the Windows system but failed."
    used_msg = "Monkey scheduled a job on the Windows system."

    query = [{'$match': {'telem_category': 'post_breach',
                         'data.name': POST_BREACH_JOB_SCHEDULING,
                         'data.command': {'$regex': 'schtasks'}}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname',
                                       'ips': ['$data.ip']},
                           'result': '$data.result'}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1053.technique_title()}

        job_scheduling_info = list(mongo.db.telemetry.aggregate(T1053.query))

        status = (ScanStatus.USED.value if job_scheduling_info[0]['result'][1]
                  else ScanStatus.SCANNED.value) if job_scheduling_info else ScanStatus.UNSCANNED.value

        data.update(T1053.get_base_data_by_status(status))
        data.update({'info': job_scheduling_info})
        return data
