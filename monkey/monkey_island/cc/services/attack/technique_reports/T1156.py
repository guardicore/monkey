from common.common_consts.post_breach_consts import POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1156(PostBreachTechnique):
    tech_id = "T1156"
    relevant_systems = ["Linux"]
    unscanned_msg = "Monkey didn't try modifying bash startup files."
    scanned_msg = "Monkey tried modifying bash startup files but failed."
    used_msg = "Monkey successfully modified bash startup files."
    pba_names = [POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION]
