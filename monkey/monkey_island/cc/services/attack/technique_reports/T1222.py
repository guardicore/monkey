from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1222(AttackTechnique):
    tech_id = "T1222"
    unscanned_msg = "Monkey didn't try to change any file permissions."
    scanned_msg = "Monkey tried to change file permissions, but failed."
    used_msg = "Monkey successfully changed file permissions in network systems."

    query = [{'$match': {'telem_category': 'attack',
                         'data.technique': 'T1222',
                         'data.status': ScanStatus.USED.value}},
             {'$lookup': {'from': 'monkey',
                          'localField': 'monkey_guid',
                          'foreignField': 'guid',
                          'as': 'monkey'}},
             {'$project': {'monkey': {'$arrayElemAt': ['$monkey', 0]},
                           'status': '$data.status',
                           'command': '$data.command'}},
             {'$addFields': {'_id': 0,
                             'machine': {'hostname': '$monkey.hostname', 'ips': '$monkey.ip_addresses'},
                             'monkey': 0}},
             {'$group': {'_id': {'machine': '$machine', 'status': '$status', 'command': '$command'}}},
             {"$replaceRoot": {"newRoot": "$_id"}}]

    @staticmethod
    def get_report_data():
        data = T1222.get_tech_base_data()
        data.update({'commands': list(mongo.db.telemetry.aggregate(T1222.query))})
        return data
