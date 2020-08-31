from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1075(AttackTechnique):
    tech_id = "T1075"
    unscanned_msg = "Monkey didn't try to use pass the hash attack since it didn't run on any Windows machines."
    scanned_msg = "Monkey tried to use hashes while logging in but didn't succeed."
    used_msg = "Monkey successfully used hashed credentials."

    login_attempt_query = {'data.attempts': {'$elemMatch': {'$or': [{'ntlm_hash': {'$ne': ''}},
                                                                    {'lm_hash': {'$ne': ''}}]}}}

    # Gets data about successful PTH logins
    query = [{'$match': {'telem_category': 'exploit',
                         'data.attempts': {'$not': {'$size': 0},
                                           '$elemMatch': {'$and': [{'$or': [{'ntlm_hash': {'$ne': ''}},
                                                                            {'lm_hash': {'$ne': ''}}]},
                                                                   {'result': True}]}}}},
             {'$project': {'_id': 0,
                           'machine': '$data.machine',
                           'info': '$data.info',
                           'attempt_cnt': {'$size': '$data.attempts'},
                           'attempts': {'$filter': {'input': '$data.attempts',
                                                    'as': 'attempt',
                                                    'cond': {'$eq': ['$$attempt.result', True]}}}}}]

    @staticmethod
    def get_report_data():
        @T1075.is_status_disabled
        def get_technique_status_and_data():
            successful_logins = list(mongo.db.telemetry.aggregate(T1075.query))
            if successful_logins:
                status = ScanStatus.USED.value
            elif mongo.db.telemetry.count_documents(T1075.login_attempt_query):
                status = ScanStatus.SCANNED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, successful_logins)

        status, successful_logins = get_technique_status_and_data()
        data = {'title': T1075.technique_title()}
        data.update({'successful_logins': successful_logins})

        data.update(T1075.get_message_and_status(status))
        data.update(T1075.get_mitigation_by_status(status))
        return data
