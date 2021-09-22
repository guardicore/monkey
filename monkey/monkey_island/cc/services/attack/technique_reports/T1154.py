from common.common_consts.post_breach_consts import POST_BREACH_TRAP_COMMAND
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1154(PostBreachTechnique):
    tech_id = "T1154"
    relevant_systems = ["Linux"]
    unscanned_msg = "Monkey didn't use the trap command."
    scanned_msg = "Monkey tried using the trap command but failed."
    used_msg = "Monkey used the trap command successfully."
    pba_names = [POST_BREACH_TRAP_COMMAND]
