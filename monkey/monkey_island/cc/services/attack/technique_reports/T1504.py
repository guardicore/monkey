from common.common_consts.post_breach_consts import POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1504(PostBreachTechnique):
    tech_id = "T1504"
    relevant_systems = ["Windows"]
    unscanned_msg = "Monkey didn't try modifying PowerShell startup files."
    scanned_msg = "Monkey tried modifying PowerShell startup files but failed."
    used_msg = "Monkey successfully modified PowerShell startup files."
    pba_names = [POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION]
