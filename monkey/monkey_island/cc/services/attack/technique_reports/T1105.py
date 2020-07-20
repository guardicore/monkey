from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1105(AttackTechnique):
    tech_id = "T1105"
    unscanned_msg = "Monkey didn't try to copy files to any systems."
    scanned_msg = "Monkey tried to copy files, but failed."
    used_msg = "Monkey successfully copied files to systems on the network."

    query = [{'$match': {'telem_category': 'attack',
                         'data.technique': tech_id}},
             {'$project': {'_id': 0,
                           'src': '$data.src',
                           'dst': '$data.dst',
                           'filename': '$data.filename'}},
             {'$group': {'_id': {'src': '$src', 'dst': '$dst', 'filename': '$filename'}}},
             {"$replaceRoot": {"newRoot": "$_id"}}]

    @staticmethod
    def get_report_data():
        data = T1105.get_tech_base_data()
        data.update({'files': list(mongo.db.telemetry.aggregate(T1105.query))})
        return data
