from common.common_consts.post_breach_consts import POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1216(PostBreachTechnique):
    tech_id = "T1216"
    relevant_systems = ["Windows"]
    unscanned_msg = (
        "Monkey didn't attempt to execute an arbitrary program with the help of a "
        "pre-existing signed script. "
    )
    scanned_msg = (
        "Monkey attempted to execute an arbitrary program with the help of a "
        "pre-existing signed script on Windows but failed. "
    )
    used_msg = (
        "Monkey executed an arbitrary program with the help of a pre-existing signed script "
        "on Windows. "
    )
    pba_names = [POST_BREACH_SIGNED_SCRIPT_PROXY_EXEC]
