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
    data = get_tech_base_data(TECHNIQUE, MESSAGES)
    found_services = get_res_by_status(ScanStatus.SCANNED.value)
    exploited_services = get_res_by_status(ScanStatus.USED.value)
    data.update({'found_services': found_services, 'exploited_services': exploited_services})
    return data


def get_res_by_status(status):
    results = mongo.db.attack_results.aggregate([{'$match': {'technique': TECHNIQUE, 'status': status}},
                                                         {'$group': {
                                                             '_id': {'ip_addr': '$machine.ip_addr',
                                                                     'port': '$port',
                                                                     'url': '$url'},
                                                             'ip_addr': {'$first': '$machine.ip_addr'},
                                                             'domain_name': {'$first': '$machine.domain_name'},
                                                             'port': {'$first': '$port'},
                                                             'url': {'$first': '$url'},
                                                             'service': {'$last': '$service'},
                                                             'time': {'$first': '$time'}}
                                                         }])
    return list(results)
