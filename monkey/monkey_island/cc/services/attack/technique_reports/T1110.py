from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.attack.technique_reports.technique_report_tools import \
    parse_creds

__author__ = "VakarisZ"


class T1110(AttackTechnique):
    tech_id = "T1110"
    unscanned_msg = "Monkey didn't try to brute force any services."
    scanned_msg = "Monkey tried to brute force some services, but failed."
    used_msg = "Monkey successfully used brute force in the network."

    # Gets data about brute force attempts
    query = [{'$match': {'telem_category': 'exploit',
                         'data.attempts': {'$not': {'$size': 0}}}},
             {'$project': {'_id': 0,
                           'machine': '$data.machine',
                           'info': '$data.info',
                           'attempt_cnt': {'$size': '$data.attempts'},
                           'attempts': {'$filter': {'input': '$data.attempts',
                                                    'as': 'attempt',
                                                    'cond': {'$eq': ['$$attempt.result', True]}}}}}]

    @staticmethod
    def get_report_data():
        @T1110.is_status_disabled
        def get_technique_status_and_data():
            attempts = list(mongo.db.telemetry.aggregate(T1110.query))
            succeeded = False

            for result in attempts:
                result['successful_creds'] = []
                for attempt in result['attempts']:
                    succeeded = True
                    result['successful_creds'].append(parse_creds(attempt))

            if succeeded:
                status = ScanStatus.USED.value
            elif attempts:
                status = ScanStatus.SCANNED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, attempts)

        status, attempts = get_technique_status_and_data()

        data = T1110.get_base_data_by_status(status)
        # Remove data with no successful brute force attempts
        attempts = [attempt for attempt in attempts if attempt['attempts']]

        data.update({'services': attempts})
        return data
