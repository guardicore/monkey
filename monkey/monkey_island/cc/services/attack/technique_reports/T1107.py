from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1107(AttackTechnique):
    tech_id = "T1107"
    unscanned_msg = ""
    scanned_msg = "Monkey tried to delete files on systems in the network, but failed."
    used_msg = "Monkey successfully deleted files on systems in the network."

    query = [{'$match': {'telem_category': 'attack',
                         'data.technique': 'T1107'}},
             {'$lookup': {'from': 'monkey',
                          'localField': 'monkey_guid',
                          'foreignField': 'guid',
                          'as': 'monkey'}},
             {'$project': {'monkey': {'$arrayElemAt': ['$monkey', 0]},
                           'status': '$data.status',
                           'path': '$data.path'}},
             {'$addFields': {'_id': 0,
                             'machine': {'hostname': '$monkey.hostname', 'ips': '$monkey.ip_addresses'},
                             'monkey': 0}},
             {'$group': {'_id': {'machine': '$machine', 'status': '$status', 'path': '$path'}}}]

    @staticmethod
    def get_report_data():
        data = T1107.get_tech_base_data()
        deleted_files = list(mongo.db.telemetry.aggregate(T1107.query))
        data.update({'deleted_files': deleted_files})
        return data
