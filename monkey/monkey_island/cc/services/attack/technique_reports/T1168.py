from common.data.post_breach_consts import POST_BREACH_JOB_SCHEDULING
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "shreyamalviya"


class T1168(AttackTechnique):
    tech_id = "T1168"
    unscanned_msg = "Monkey did not try scheduling a job on Linux."
    scanned_msg = "Monkey tried scheduling a job on the Linux system but failed."
    used_msg = "Monkey scheduled a job on the Linux system."

    query = [{'$match': {'telem_category': 'post_breach',
                         'data.name': POST_BREACH_JOB_SCHEDULING,
                         'data.command': {'$regex': 'crontab'}}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname',
                                       'ips': '$data.ip'},
                           'result': '$data.result'}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1168.technique_title()}

        job_scheduling_info = list(mongo.db.telemetry.aggregate(T1168.query))

        status = ScanStatus.UNSCANNED.value
        if job_scheduling_info:
            successful_PBAs = mongo.db.telemetry.count({'data.name': POST_BREACH_JOB_SCHEDULING,
                                                        'data.result.1': True})
            status = ScanStatus.USED.value if successful_PBAs else ScanStatus.SCANNED.value

        data.update(T1168.get_base_data_by_status(status))
        data.update({'info': job_scheduling_info})
        return data
