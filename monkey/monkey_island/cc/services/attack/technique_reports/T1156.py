from common.data.post_breach_consts import \
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.attack.technique_reports.technique_report_tools import \
    extract_shell_startup_files_modification_info, get_shell_startup_files_modification_status

__author__ = "shreyamalviya"


class T1156(AttackTechnique):
    tech_id = "T1156"
    unscanned_msg = "Monkey did not try modifying bash startup files on the system."
    scanned_msg = "Monkey tried modifying bash startup files on the system but failed."
    used_msg = "Monkey modified bash startup files on the system."

    query = [{'$match': {'telem_category': 'post_breach',
                         'data.name': POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION}},
             {'$project': {'_id': 0,
                           'machine': {'hostname': '$data.hostname',
                                       'ips': ['$data.ip']},
                           'result': '$data.result'}}]

    @staticmethod
    def get_report_data():
        data = {'title': T1156.technique_title(), 'info': []}

        shell_startup_files_modification_info = list(mongo.db.telemetry.aggregate(T1156.query))

        bash_startup_modification_info =\
            extract_shell_startup_files_modification_info(shell_startup_files_modification_info, [".bash", ".profile"])

        status = get_shell_startup_files_modification_status(bash_startup_modification_info)

        data.update(T1156.get_base_data_by_status(status))
        data.update({'info': bash_startup_modification_info})
        return data
