from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1059(AttackTechnique):

    tech_id = "T1059"
    unscanned_msg = "Monkey didn't exploit any machines to run commands at."
    scanned_msg = ""
    used_msg = "Monkey successfully ran commands on exploited machines in the network."

    query = [{'$match': {'telem_type': 'exploit',
                         'data.info.executed_cmds.example': {'$exists': True}}},
             {'$project': {'_id': 0,
                           'machine': '$data.machine',
                           'info': '$data.info'}},
             {'$group': {'_id': '$machine', 'data': {'$push': '$$ROOT'}}}]

    @staticmethod
    def get_report_data():
        cmd_data = list(mongo.db.telemetry.aggregate(T1059.query))
        data = {'title': T1059.technique_title(), 'cmds': cmd_data}
        if cmd_data:
            status = ScanStatus.USED
        else:
            status = ScanStatus.UNSCANNED
        data.update(T1059.get_message_and_status(status))
        return data
