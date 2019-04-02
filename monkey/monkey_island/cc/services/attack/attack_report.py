import logging
from cc.services.attack.technique_reports import T1210

__author__ = "VakarisZ"


logger = logging.getLogger(__name__)


class AttackReportService:
    def __init__(self):
        pass

    @staticmethod
    def get_report():
        report = {}
        report.update({'T1210': T1210.get_report_data()})
        return report
