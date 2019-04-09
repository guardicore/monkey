from monkey_island.cc.services.attack.technique_reports.technique_service import *
from cc.services.report import ReportService

__author__ = "VakarisZ"

TECHNIQUE = "T1210"
MESSAGES = {
    'unscanned': "Monkey didn't scan any remote services. Maybe it didn't find any machines on the network?",
    'scanned': "Monkey scanned for remote services on the network, but couldn't exploit any of them.",
    'used': "Monkey scanned for remote services and exploited some on the network."
}


def get_report_data():
    data = get_tech_base_data(TECHNIQUE, MESSAGES)
    data.update({'scanned_machines': ReportService.get_scanned()})
    data.update({'exploited_machines': ReportService.get_exploited()})
    return data

