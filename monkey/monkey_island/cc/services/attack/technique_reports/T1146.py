from common.common_consts.post_breach_consts import POST_BREACH_CLEAR_CMD_HISTORY
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1146(PostBreachTechnique):
    tech_id = "T1146"
    relevant_systems = ["Linux"]
    unscanned_msg = "Monkey didn't try clearing the command history on a Linux system."
    scanned_msg = "Monkey tried clearing the command history on a Linux system but failed."
    used_msg = (
        "Monkey successfully cleared the command history on a Linux system (and then "
        "restored it back)."
    )
    pba_names = [POST_BREACH_CLEAR_CMD_HISTORY]
