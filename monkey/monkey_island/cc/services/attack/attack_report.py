import logging
from cc.services.attack.technique_reports import T1210
from cc.services.attack.attack_telem import get_latest_telem
from cc.database import mongo

__author__ = "VakarisZ"


logger = logging.getLogger(__name__)

TECHNIQUES = {'T1210': T1210}

class AttackReportService:
    def __init__(self):
        pass

    @staticmethod
    def generate_new_report():
        report = {'techniques': {}, 'meta': {get_latest_telem()}}
        for tech_id, value in
        report.update({'T1210': T1210.get_report_data()})
        report.update({''})
        return report

    @staticmethod
    def get_latest_report():
        if AttackReportService.is_report_generated():
            telem_time = get_latest_telem_time()
            lates_report = mongo.db.attack_report.find_one({'name': 'new_report'})
            if telem_time == lates_report['telem_time']:
                return lates_report
        return AttackReportService.generate_new_report()

    @staticmethod
    def is_report_generated():
        generated_report = mongo.db.attack_report.find_one({})
        return generated_report is not None
