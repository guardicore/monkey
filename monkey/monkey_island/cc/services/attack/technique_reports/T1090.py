from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1090(AttackTechnique):

    tech_id = "T1090"
    unscanned_msg = "Monkey didn't use connection proxy."
    scanned_msg = ""
    used_msg = "Monkey used connection proxy."

    query = [{'$match': {'telem_category': 'exploit',
                         'data.info.executed_cmds': {'$exists': True, '$ne': []}}},
             {'$unwind': '$data.info.executed_cmds'},
             {'$sort': {'data.info.executed_cmds.powershell': 1}},
             {'$project': {'_id': 0,
                           'machine': '$data.machine',
                           'info': '$data.info'}},
             {'$group': {'_id': '$machine', 'data': {'$push': '$$ROOT'}}},
             {'$project': {'_id': 0, 'data': {'$arrayElemAt': ['$data', 0]}}}]

    @staticmethod
    def get_report_data():
        cmd_data = list(mongo.db.telemetry.aggregate(T1090.query))
        data = {'title': T1090.technique_title(), 'cmds': cmd_data}
        if cmd_data:
            status = ScanStatus.USED.value
        else:
            status = ScanStatus.UNSCANNED.value
        data.update(T1090.get_message_and_status(status))
        return data
