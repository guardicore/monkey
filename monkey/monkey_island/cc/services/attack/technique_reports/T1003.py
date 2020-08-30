from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.reporting.report import ReportService

__author__ = "VakarisZ"


class T1003(AttackTechnique):
    tech_id = "T1003"
    unscanned_msg = "Monkey tried to obtain credentials from systems in the network but didn't find any or failed."
    scanned_msg = ""
    used_msg = "Monkey successfully obtained some credentials from systems on the network."

    query = {'telem_category': 'system_info', '$and': [{'data.credentials': {'$exists': True}},
                                                       # $gt: {} checks if field is not an empty object
                                                       {'data.credentials': {'$gt': {}}}]}

    @staticmethod
    def get_report_data():
        @T1003.is_status_disabled
        def get_technique_status_and_data():
            if mongo.db.telemetry.count_documents(T1003.query):
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, [])

        data = {'title': T1003.technique_title()}
        status, _ = get_technique_status_and_data()

        data.update(T1003.get_message_and_status(status))
        data.update(T1003.get_mitigation_by_status(status))
        data['stolen_creds'] = ReportService.get_stolen_creds()
        data['stolen_creds'].extend(ReportService.get_ssh_keys())
        return data
