from common.data.post_breach_consts import \
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1156(PostBreachTechnique):
    tech_id = "T1156"
    unscanned_msg = "Monkey did not try modifying bash startup files on the system."
    scanned_msg = "Monkey tried modifying bash startup files on the system but failed."
    used_msg = "Monkey modified bash startup files on the system."
    pba_names = [POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION]
