from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1075(AttackTechnique):

    tech_id = "T1075"
    unscanned_msg = "Monkey didn't try to use pass the hash attack."
    scanned_msg = "Monkey tried to use hashes while logging in but didn't succeed."
    used_msg = "Monkey successfully used hashed credentials."

    login_attempt_query = {'data.attempts': {'$elemMatch': {'$or': [{'ntlm_hash': {'$ne': ''}},
                                                                    {'lm_hash': {'$ne': ''}}]}}}

    # Gets data about successful PTH logins
    query = [{'$match': {'telem_type': 'exploit',
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
        data = {'title': T1075.technique_title(T1075.tech_id)}
        successful_logins = list(mongo.db.telemetry.aggregate(T1075.query))
        data.update({'successful_logins': successful_logins})
        if successful_logins:
            data.update({'message': T1075.used_msg, 'status': ScanStatus.USED.name})
        elif mongo.db.telemetry.count_documents(T1075.login_attempt_query):
            data.update({'message': T1075.scanned_msg, 'status': ScanStatus.SCANNED.name})
        else:
            data.update({'message': T1075.unscanned_msg, 'status': ScanStatus.UNSCANNED.name})
        return data
