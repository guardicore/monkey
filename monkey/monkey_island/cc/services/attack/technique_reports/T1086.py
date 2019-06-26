from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1086(AttackTechnique):

    tech_id = "T1086"
    unscanned_msg = "Monkey didn't run powershell."
    scanned_msg = ""
    used_msg = "Monkey successfully ran powershell commands on exploited machines in the network."

    query = [{'$match': {'telem_category': 'exploit',
                         'data.info.executed_cmds': {'$elemMatch': {'powershell': True}}}},
             {'$project': {'machine': '$data.machine',
                           'info': '$data.info'}},
             {'$project': {'_id': 0,
                           'machine': 1,
                           'info.finished': 1,
                           'info.executed_cmds': {'$filter': {'input': '$info.executed_cmds',
                                                              'as': 'command',
                                                              'cond': {'$eq': ['$$command.powershell', True]}}}}},
             {'$group': {'_id': '$machine', 'data': {'$push': '$$ROOT'}}}]

    @staticmethod
    def get_report_data():
        cmd_data = list(mongo.db.telemetry.aggregate(T1086.query))
        data = {'title': T1086.technique_title(), 'cmds': cmd_data}
        if cmd_data:
            status = ScanStatus.USED
        else:
            status = ScanStatus.UNSCANNED
        data.update(T1086.get_message_and_status(status))
        return data
