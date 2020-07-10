from common.data.post_breach_consts import \
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1504(PostBreachTechnique):
    tech_id = "T1504"
    unscanned_msg = "Monkey did not try modifying powershell startup files on the system."
    scanned_msg = "Monkey tried modifying powershell startup files on the system but failed."
    used_msg = "Monkey modified powershell startup files on the system."
    pba_names = [POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION]
