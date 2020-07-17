from common.data.post_breach_consts import \
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from monkey_island.cc.services.attack.technique_reports.pba_technique import \
    PostBreachTechnique

__author__ = "shreyamalviya"


class T1504(PostBreachTechnique):
    tech_id = "T1504"
    unscanned_msg = "Monkey didn't try modifying powershell startup files since it found no Windows machines."
    scanned_msg = "Monkey tried modifying powershell startup files but failed."
    used_msg = "Monkey successfully modified powershell startup files."
    pba_names = [POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION]
