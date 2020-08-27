from common.data.post_breach_consts import POST_BREACH_ACCOUNT_DISCOVERY
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1087(PostBreachTechnique):
    tech_id = "T1087"
    unscanned_msg = "Monkey didn't try to get a listing of user accounts."
    scanned_msg = "Monkey tried to get a listing of user accounts but failed to do so."
    used_msg = "Monkey got a listing of user accounts successfully."
    pba_names = [POST_BREACH_ACCOUNT_DISCOVERY]
