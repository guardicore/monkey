from common.data.post_breach_consts import (
    POST_BREACH_BACKDOOR_USER, POST_BREACH_COMMUNICATE_AS_NEW_USER)
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1136(PostBreachTechnique):
    tech_id = "T1136"
    unscanned_msg = "Monkey didn't try creating a new user on the network's systems."
    scanned_msg = "Monkey tried creating a new user on the network's systems, but failed."
    used_msg = "Monkey created a new user on the network's systems."
    pba_names = [POST_BREACH_BACKDOOR_USER, POST_BREACH_COMMUNICATE_AS_NEW_USER]
