from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1086(AttackTechnique):

    tech_id = "T1086"
    unscanned_msg = "Monkey didn't run powershell."
    scanned_msg = ""
    used_msg = "Monkey successfully ran powershell commands on exploited machines in the network."

    query = [{'$match': {'telem_type': 'exploit',
                         'data.info.executed_cmds.powershell': {'$exists': True}}},
             {'$project': {'_id': 0,
                           'machine': '$data.machine',
                           'info': '$data.info'}},
             {'$group': {'_id': '$machine', 'data': {'$push': '$$ROOT'}}}]

    @staticmethod
    def get_report_data():
        cmd_data = list(mongo.db.telemetry.aggregate(T1086.query))
        data = {'title': T1086.technique_title(T1086.tech_id), 'cmds': cmd_data}
        if cmd_data:
            data.update({'message': T1086.used_msg, 'status': ScanStatus.USED.name})
        else:
            data.update({'message': T1086.unscanned_msg, 'status': ScanStatus.UNSCANNED.name})
        return data
