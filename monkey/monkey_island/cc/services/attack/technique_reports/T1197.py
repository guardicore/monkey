from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1197(AttackTechnique):
    tech_id = "T1197"
    unscanned_msg = "Monkey didn't try to use any bits jobs."
    scanned_msg = "Monkey tried to use bits jobs but failed."
    used_msg = "Monkey successfully used bits jobs at least once in the network."

    @staticmethod
    def get_report_data():
        data = T1197.get_tech_base_data(T1197)
        bits_results = mongo.db.attack_results.aggregate([{'$match': {'technique': T1197.tech_id}},
                                                          {'$group': {'_id': {'ip_addr': '$machine.ip_addr', 'usage': '$usage'},
                                                                      'ip_addr': {'$first': '$machine.ip_addr'},
                                                                      'domain_name': {'$first': '$machine.domain_name'},
                                                                      'usage': {'$first': '$usage'},
                                                                      'time': {'$first': '$time'}}
                                                           }])
        bits_results = list(bits_results)
        data.update({'bits_jobs': bits_results})
        return data
