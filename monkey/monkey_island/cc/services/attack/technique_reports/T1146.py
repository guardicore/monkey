from common.data.post_breach_consts import POST_BREACH_CLEAR_CMD_HISTORY
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1146(PostBreachTechnique):
    tech_id = "T1146"
    unscanned_msg = "Monkey didn't try clearing the command history since it didn't run on any Linux machines."
    scanned_msg = "Monkey tried clearing the command history but failed."
    used_msg = "Monkey successfully cleared the command history (and then restored it back)."
    pba_names = [POST_BREACH_CLEAR_CMD_HISTORY]

    @staticmethod
    def get_pba_query(*args):
        return [{'$match': {'telem_category': 'post_breach',
                            'data.name': POST_BREACH_CLEAR_CMD_HISTORY}},
                {'$project': {'_id': 0,
                              'machine': {'hostname': {'$arrayElemAt': ['$data.hostname', 0]},
                                          'ips': [{'$arrayElemAt': ['$data.ip', 0]}]},
                              'result': '$data.result'}}]
