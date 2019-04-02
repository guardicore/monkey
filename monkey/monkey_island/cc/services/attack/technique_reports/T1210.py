from monkey_island.cc.services.attack.technique_reports.technique_service import technique_status, technique_title
from common.utils.attack_status_enum import ScanStatus
from cc.services.report import ReportService

__author__ = "VakarisZ"

TECHNIQUE = "T1210"
UNSCANNED_MSG = "Monkey didn't scan any remote services. Maybe it didn't find any machines on the network?"
SCANNED_MSG = "Monkey scanned for remote services on the network, but couldn't exploit any of them."
USED_MSG = "Monkey scanned for remote services and exploited some on the network."


def get_report_data():
    data = {}
    status = technique_status(TECHNIQUE)
    title = technique_title(TECHNIQUE)
    data.update({'status': status.name, 'title': title})
    if status == ScanStatus.UNSCANNED:
        data.update({'message': UNSCANNED_MSG})
        return data
    elif status == ScanStatus.SCANNED:
        data.update({'message': SCANNED_MSG})
    else:
        data.update({'message': USED_MSG})
    data.update({'scanned_machines': ReportService.get_scanned()})
    data.update({'exploited_machines': ReportService.get_exploited()})
    return data

