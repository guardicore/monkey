from common.data.post_breach_consts import \
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1156(PostBreachTechnique):
    tech_id = "T1156"
    unscanned_msg = "Monkey didn't try modifying bash startup files since it didn't run on any Linux machines."
    scanned_msg = "Monkey tried modifying bash startup files but failed."
    used_msg = "Monkey successfully modified bash startup files."
    pba_names = [POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION]

    @staticmethod
    def get_pba_query(*args):
        return [{'$match': {'telem_category': 'post_breach',
                            'data.name': POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION}},
                {'$project': {'_id': 0,
                              'machine': {'hostname': {'$arrayElemAt': ['$data.hostname', 0]},
                                          'ips': [{'$arrayElemAt': ['$data.ip', 0]}]},
                              'result': '$data.result'}},
                {'$unwind': '$result'},
                {'$match': {'$or': [{'result': {'$regex': r'\.bash'}},
                                    {'result': {'$regex': r'\.profile'}}]}}]
