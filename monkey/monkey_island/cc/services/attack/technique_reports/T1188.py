from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.models.monkey import Monkey

__author__ = "VakarisZ"


class T1188(AttackTechnique):

    tech_id = "T1188"
    unscanned_msg = "Monkey didn't use multi-hop proxy."
    scanned_msg = ""
    used_msg = "Monkey used multi-hop proxy."

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
        monkeys = T1188.get_tunneled_monkeys()
        for monkey in monkeys:
            proxy_chain = 0
            proxy = Monkey.objects(id=monkey.tunnel)
            while proxy:
                proxy_chain += 1
                proxy = Monkey.objects(id=monkey.tunnel)

        data = {'title': T1188.technique_title()}
        return data

    @staticmethod
    def get_tunneled_monkeys():
        return Monkey.objects(tunnel__exists=True)
