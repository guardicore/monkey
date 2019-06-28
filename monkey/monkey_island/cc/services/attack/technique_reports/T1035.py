from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1035(AttackTechnique):
    tech_id = "T1035"
    unscanned_msg = "Monkey didn't try to interact with Windows services."
    scanned_msg = "Monkey tried to interact with Windows services, but failed."
    used_msg = "Monkey successfully interacted with Windows services."

    query = [{'$match': {'telem_category': 'attack',
                         'data.technique': tech_id}},
             {'$lookup': {'from': 'monkey',
                          'localField': 'monkey_guid',
                          'foreignField': 'guid',
                          'as': 'monkey'}},
             {'$project': {'monkey': {'$arrayElemAt': ['$monkey', 0]},
                           'status': '$data.status',
                           'usage': '$data.usage'}},
             {'$addFields': {'_id': 0,
                             'machine': {'hostname': '$monkey.hostname', 'ips': '$monkey.ip_addresses'},
                             'monkey': 0}},
             {'$group': {'_id': {'machine': '$machine', 'status': '$status', 'usage': '$usage'}}}]

    @staticmethod
    def get_report_data():
        data = T1035.get_tech_base_data()
        data.update({'services': list(mongo.db.telemetry.aggregate(T1035.query))})
        return data
