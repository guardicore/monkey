from common.utils.attack_utils import ScanStatus
from monkey_island.cc.models import StolenCredentials
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.reporting.stolen_credentials import get_stolen_creds


class T1003(AttackTechnique):
    tech_id = "T1003"
    relevant_systems = ["Linux", "Windows"]
    unscanned_msg = (
        "Monkey tried to obtain credentials from systems in the network but didn't "
        "find any or failed."
    )
    scanned_msg = ""
    used_msg = "Monkey successfully obtained some credentials from systems on the network."

    @staticmethod
    def get_report_data():
        def get_technique_status_and_data():
            if list(StolenCredentials.objects()):
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, [])

        data = {"title": T1003.technique_title()}
        status, _ = get_technique_status_and_data()

        data.update(T1003.get_message_and_status(status))
        data.update(T1003.get_mitigation_by_status(status))
        data["stolen_creds"] = get_stolen_creds()
        return data
