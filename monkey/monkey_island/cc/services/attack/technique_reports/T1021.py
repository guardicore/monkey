from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.attack.technique_reports.technique_report_tools import \
    parse_creds

__author__ = "VakarisZ"


class T1021(AttackTechnique):
    tech_id = "T1021"
    unscanned_msg = "Monkey didn't try to login to any remote services."
    scanned_msg = "Monkey tried to login to remote services with valid credentials, but failed."
    used_msg = "Monkey successfully logged into remote services on the network."

    # Gets data about brute force attempts
    query = [{'$match': {'telem_category': 'exploit',
                         'data.attempts': {'$not': {'$size': 0}}}},
             {'$project': {'_id': 0,
                           'machine': '$data.machine',
                           'info': '$data.info',
                           'attempt_cnt': {'$size': '$data.attempts'},
                           'attempts': {'$filter': {'input': '$data.attempts',
                                                    'as': 'attempt',
                                                    'cond': {'$eq': ['$$attempt.result', True]}
                                                    }
                                        }
                           }
              }]

    scanned_query = {'telem_category': 'exploit',
                     'data.attempts': {'$elemMatch': {'result': True}}}

    @staticmethod
    def get_report_data():
        @T1021.is_status_disabled
        def get_technique_status_and_data():
            attempts = []
            if mongo.db.telemetry.count_documents(T1021.scanned_query):
                attempts = list(mongo.db.telemetry.aggregate(T1021.query))
                if attempts:
                    status = ScanStatus.USED.value
                    for result in attempts:
                        result['successful_creds'] = []
                        for attempt in result['attempts']:
                            result['successful_creds'].append(parse_creds(attempt))
                else:
                    status = ScanStatus.SCANNED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, attempts)

        status, attempts = get_technique_status_and_data()

        data = T1021.get_base_data_by_status(status)
        data.update({'services': attempts})
        return data
