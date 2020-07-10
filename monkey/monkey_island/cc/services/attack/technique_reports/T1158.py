from common.data.post_breach_consts import POST_BREACH_HIDDEN_FILES
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "shreyamalviya"


class T1158(PostBreachTechnique):
    tech_id = "T1158"
    unscanned_msg = "Monkey did not try creating hidden files or folders."
    scanned_msg = "Monkey tried creating hidden files and folders on the system but failed."
    used_msg = "Monkey created hidden files and folders on the system."
    pba_name = POST_BREACH_HIDDEN_FILES
