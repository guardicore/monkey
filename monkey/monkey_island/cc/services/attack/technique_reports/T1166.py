from common.data.post_breach_consts import POST_BREACH_SETUID_SETGID
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1166(PostBreachTechnique):
    tech_id = "T1166"
    unscanned_msg = "Monkey didn't try setting the setuid or setgid bits since it didn't run on any Linux machines."
    scanned_msg = "Monkey tried setting the setuid or setgid bits but failed."
    used_msg = "Monkey successfully set the setuid or setgid bits."
    pba_names = [POST_BREACH_SETUID_SETGID]
