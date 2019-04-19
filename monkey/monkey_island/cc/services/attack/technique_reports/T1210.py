from monkey_island.cc.services.attack.technique_reports.technique_service import *
from common.utils.attack_utils import ScanStatus

__author__ = "VakarisZ"

TECHNIQUE = "T1210"
MESSAGES = {
    'unscanned': "Monkey didn't scan any remote services. Maybe it didn't find any machines on the network?",
    'scanned': "Monkey scanned for remote services on the network, but couldn't exploit any of them.",
    'used': "Monkey scanned for remote services and exploited some on the network."
}


def get_report_data():
    data = {'title': technique_title(TECHNIQUE)}
    scanned_services = get_scanned_services()
    exploited_services = get_exploited_services()
    if exploited_services:
        data.update({'status': ScanStatus.USED.name, 'message': MESSAGES['used']})
    elif scanned_services:
        data.update({'status': ScanStatus.SCANNED.name, 'message': MESSAGES['scanned']})
    else:
        data.update({'status': ScanStatus.UNSCANNED.name, 'message': MESSAGES['unscanned']})
    data.update({'scanned_services': scanned_services, 'exploited_services': exploited_services})
    return data


def get_scanned_services():
    results = mongo.db.telemetry.aggregate([{'$match': {'telem_type': 'scan'}},
                                           {'$sort': {'data.service_count': -1}},
                                           {'$group': {
                                                '_id': {'ip_addr': '$data.machine.ip_addr'},
                                                'machine': {'$first': '$data.machine'},
                                                'time': {'$first': '$timestamp'}}}])
    return list(results)


def get_exploited_services():
    results = mongo.db.telemetry.aggregate([{'$match': {'telem_type': 'exploit', 'data.result': True}},
                                            {'$group': {
                                                '_id': {'ip_addr': '$data.machine.ip_addr'},
                                                'service': {'$first': '$data.info'},
                                                'machine': {'$first': '$data.machine'},
                                                'time': {'$first': '$timestamp'}}}])
    return list(results)
