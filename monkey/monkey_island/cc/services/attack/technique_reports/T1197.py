from monkey_island.cc.services.attack.technique_reports.technique_service import *
from cc.services.report import ReportService

__author__ = "VakarisZ"

TECHNIQUE = "T1197"
MESSAGES = {
    'unscanned': "Monkey didn't try to use any bits jobs.",
    'scanned': "Monkey tried to use bits jobs but failed.",
    'used': "Monkey successfully used bits jobs at least once in the network."
}


def get_report_data():
    data = get_tech_base_data(TECHNIQUE, MESSAGES)

    data.update()
    return data
