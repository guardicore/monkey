from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.exploit_enum import ExploitType

__author__ = "VakarisZ"


class T1110(AttackTechnique):
    tech_id = "T1110"
    unscanned_msg = "Monkey didn't try to brute force any services."
    scanned_msg = "Monkey tried to brute force some services, but failed."
    used_msg = "Monkey successfully used brute force in the network."

    @staticmethod
    def get_report_data():
        data = {'title': T1110.technique_title(T1110.tech_id)}
        results = mongo.db.telemetry.find({'telem_type': 'exploit', 'data.info.exploit_type': ExploitType.BRUTE_FORCE.name, 'data.attempts': {'$ne': '[]'}},
                             {'data.machine': 1, 'data.info': 1, 'data.attempts': 1})
        results = [result['data'] for result in results]
        data.update({'services': results})
        return data
