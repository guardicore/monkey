from common.data.post_breach_consts import POST_BREACH_HIDDEN_FILES
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1158(PostBreachTechnique):
    tech_id = "T1158"
    unscanned_msg = "Monkey didn't try creating hidden files or folders."
    scanned_msg = "Monkey tried creating hidden files and folders on the system but failed."
    used_msg = "Monkey created hidden files and folders on the system."
    pba_names = [POST_BREACH_HIDDEN_FILES]
