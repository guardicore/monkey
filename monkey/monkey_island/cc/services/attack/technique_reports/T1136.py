from common.common_consts.post_breach_consts import POST_BREACH_COMMUNICATE_AS_BACKDOOR_USER
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1136(PostBreachTechnique):
    tech_id = "T1136"
    relevant_systems = ["Linux", "Windows"]
    unscanned_msg = "Monkey didn't try creating a new user on the network's systems."
    scanned_msg = "Monkey tried creating a new user on the network's systems, but failed."
    used_msg = "Monkey created a new user on the network's systems."
    pba_names = [POST_BREACH_COMMUNICATE_AS_BACKDOOR_USER]
