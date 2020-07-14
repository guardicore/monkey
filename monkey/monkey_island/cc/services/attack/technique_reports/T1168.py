from common.data.post_breach_consts import POST_BREACH_JOB_SCHEDULING
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1168(PostBreachTechnique):
    tech_id = "T1168"
    unscanned_msg = "Monkey did not try scheduling a job on Linux."
    scanned_msg = "Monkey tried scheduling a job on the Linux system but failed."
    used_msg = "Monkey scheduled a job on the Linux system."
    pba_names = [POST_BREACH_JOB_SCHEDULING]
