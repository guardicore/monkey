from common.utils.attack_utils import ScanStatus
from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.reporting import format_creds_for_reporting


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
        raise NotImplementedError


class T1003GetReportData:
    """
    Class to patch the T1003 attack technique which
    needs stolen credentials from db.
    """

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def __call__(self):
        def get_technique_status_and_data():
            if list(self._credentials_repository.get_stolen_credentials()):
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, [])

        data = {"title": T1003.technique_title()}
        status, _ = get_technique_status_and_data()

        data.update(T1003.get_message_and_status(status))
        data["stolen_creds"] = format_creds_for_reporting(
            self._credentials_repository.get_stolen_credentials()
        )
        return data
