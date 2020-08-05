from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1086(AttackTechnique):
    tech_id = "T1086"
    unscanned_msg = "Monkey didn't run powershell since it didn't run on any Windows machines."
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
        @T1086.is_status_disabled
        def get_technique_status_and_data():
            cmd_data = list(mongo.db.telemetry.aggregate(T1086.query))
            if cmd_data:
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, cmd_data)

        status, cmd_data = get_technique_status_and_data()
        data = {'title': T1086.technique_title(), 'cmds': cmd_data}

        data.update(T1086.get_mitigation_by_status(status))
        data.update(T1086.get_message_and_status(status))
        return data
