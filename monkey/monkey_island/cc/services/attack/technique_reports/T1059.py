from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1059(AttackTechnique):
    tech_id = "T1059"
    unscanned_msg = "Monkey didn't exploit any machines to run commands at."
    scanned_msg = ""
    used_msg = "Monkey successfully ran commands on exploited machines in the network."

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
        @T1059.is_status_disabled
        def get_technique_status_and_data():
            cmd_data = list(mongo.db.telemetry.aggregate(T1059.query))
            if cmd_data:
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, cmd_data)

        status, cmd_data = get_technique_status_and_data()
        data = {'title': T1059.technique_title(), 'cmds': cmd_data}

        data.update(T1059.get_message_and_status(status))
        data.update(T1059.get_mitigation_by_status(status))
        return data
