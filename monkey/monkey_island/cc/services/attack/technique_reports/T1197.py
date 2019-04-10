from monkey_island.cc.services.attack.technique_reports.technique_service import *
from cc.database import mongo

__author__ = "VakarisZ"

TECHNIQUE = "T1197"
MESSAGES = {
    'unscanned': "Monkey didn't try to use any bits jobs.",
    'scanned': "Monkey tried to use bits jobs but failed.",
    'used': "Monkey successfully used bits jobs at least once in the network."
}


def get_report_data():
    data = get_tech_base_data(TECHNIQUE, MESSAGES)
    bits_results = mongo.db.attack_results.aggregate([{'$match': {'technique': TECHNIQUE}},
                                                      {'$group': {'_id': {'ip_addr': '$machine.ip_addr', 'usage': '$usage'},
                                                                  'ip_addr': {'$first': '$machine.ip_addr'},
                                                                  'domain_name': {'$first': '$machine.domain_name'},
                                                                  'usage': {'$first': '$usage'},
                                                                  'time': {'$first': '$time'}}
                                                       }])
    bits_results = list(bits_results)
    data.update({'bits_jobs': bits_results})
    return data
