from common.data.post_breach_consts import POST_BREACH_JOB_SCHEDULING
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1053(PostBreachTechnique):
    tech_id = "T1053"
    unscanned_msg = "Monkey didn't try scheduling a job on Windows since it didn't run on any Windows machines."
    scanned_msg = "Monkey tried scheduling a job on the Windows system but failed."
    used_msg = "Monkey scheduled a job on the Windows system."
    pba_names = [POST_BREACH_JOB_SCHEDULING]
