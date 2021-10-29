from common.common_consts.post_breach_consts import POST_BREACH_JOB_SCHEDULING
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1053(PostBreachTechnique):
    tech_id = "T1053"
    relevant_systems = ["Windows"]
    unscanned_msg = "Monkey didn't try scheduling a job on any Windows system."
    scanned_msg = "Monkey tried scheduling a job on a Windows system but failed."
    used_msg = "Monkey scheduled a job on a Windows system."
    pba_names = [POST_BREACH_JOB_SCHEDULING]
