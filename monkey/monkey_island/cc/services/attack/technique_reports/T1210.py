from monkey_island.cc.services.attack.technique_reports.technique_service import *
from cc.services.report import ReportService
from common.utils.attack_utils import ScanStatus

__author__ = "VakarisZ"

TECHNIQUE = "T1210"
MESSAGES = {
    'unscanned': "Monkey didn't scan any remote services. Maybe it didn't find any machines on the network?",
    'scanned': "Monkey scanned for remote services on the network, but couldn't exploit any of them.",
    'used': "Monkey scanned for remote services and exploited some on the network."
}


def get_report_data():
    data = {}
    scanned_machines = ReportService.get_scanned()
    exploited_machines = ReportService.get_exploited()
    data.update({'message': MESSAGES['unscanned'], 'status': ScanStatus.UNSCANNED.name})
    for machine in scanned_machines:
        if machine['services']:
            data.update({'message': MESSAGES['scanned'], 'status': ScanStatus.SCANNED.name})
    for machine in exploited_machines:
        if machine['exploits']:
            data.update({'message': MESSAGES['used'], 'status': ScanStatus.USED.name})
    data.update({'technique': TECHNIQUE, 'title': technique_title(TECHNIQUE)})
    data.update({'scanned_machines': scanned_machines})
    data.update({'exploited_machines': exploited_machines})
    return data

