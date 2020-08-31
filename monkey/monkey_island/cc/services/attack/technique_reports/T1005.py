from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1005(AttackTechnique):
    tech_id = "T1005"
    unscanned_msg = "Monkey didn't gather any sensitive data from local system."
    scanned_msg = ""
    used_msg = "Monkey successfully gathered sensitive data from local system."

    query = [{'$match': {'telem_category': 'attack',
                         'data.technique': tech_id}},
             {'$lookup': {'from': 'monkey',
                          'localField': 'monkey_guid',
                          'foreignField': 'guid',
                          'as': 'monkey'}},
             {'$project': {'monkey': {'$arrayElemAt': ['$monkey', 0]},
                           'status': '$data.status',
                           'gathered_data_type': '$data.gathered_data_type',
                           'info': '$data.info'}},
             {'$addFields': {'_id': 0,
                             'machine': {'hostname': '$monkey.hostname', 'ips': '$monkey.ip_addresses'},
                             'monkey': 0}},
             {'$group': {'_id': {'machine': '$machine', 'gathered_data_type': '$gathered_data_type', 'info': '$info'}}},
             {"$replaceRoot": {"newRoot": "$_id"}}]

    @staticmethod
    def get_report_data():
        data = T1005.get_tech_base_data()
        data.update({'collected_data': list(mongo.db.telemetry.aggregate(T1005.query))})
        return data
