from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1003(AttackTechnique):

    tech_id = "T1003"
    unscanned_msg = "Monkey tried to obtain credentials from systems in the network but didn't find any or failed."
    scanned_msg = ""
    used_msg = "Monkey successfully obtained some credentials from systems on the network."

    query = {'telem_category': 'system_info_collection', '$and': [{'data.credentials': {'$exists': True}},
                                                                  # $gt: {} checks if field is not an empty object
                                                                  {'data.credentials': {'$gt': {}}}]}

    @staticmethod
    def get_report_data():
        data = {'title': T1003.technique_title()}
        if mongo.db.telemetry.count_documents(T1003.query):
            status = ScanStatus.USED
        else:
            status = ScanStatus.UNSCANNED
        data.update(T1003.get_message_and_status(status))
        return data
