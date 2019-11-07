from common.utils.attack_utils import ScanStatus
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.database import mongo

__author__ = "VakarisZ"


class T1210(AttackTechnique):
    tech_id = "T1210"
    unscanned_msg = "Monkey didn't scan any remote services. Maybe it didn't find any machines on the network?"
    scanned_msg = "Monkey scanned for remote services on the network, but couldn't exploit any of them."
    used_msg = "Monkey scanned for remote services and exploited some on the network."

    @staticmethod
    def get_report_data():
        data = {'title': T1210.technique_title()}
        scanned_services = T1210.get_scanned_services()
        exploited_services = T1210.get_exploited_services()
        if exploited_services:
            status = ScanStatus.USED.value
        elif scanned_services:
            status = ScanStatus.SCANNED.value
        else:
            status = ScanStatus.UNSCANNED.value
        data.update(T1210.get_message_and_status(status))
        data.update({'scanned_services': scanned_services, 'exploited_services': exploited_services})
        return data

    @staticmethod
    def get_scanned_services():
        results = mongo.db.telemetry.aggregate([{'$match': {'telem_category': 'scan'}},
                                                {'$sort': {'data.service_count': -1}},
                                                {'$group': {
                                                    '_id': {'ip_addr': '$data.machine.ip_addr'},
                                                    'machine': {'$first': '$data.machine'},
                                                    'time': {'$first': '$timestamp'}}}])
        return list(results)

    @staticmethod
    def get_exploited_services():
        results = mongo.db.telemetry.aggregate([{'$match': {'telem_category': 'exploit', 'data.result': True}},
                                                {'$group': {
                                                    '_id': {'ip_addr': '$data.machine.ip_addr'},
                                                    'service': {'$first': '$data.info'},
                                                    'machine': {'$first': '$data.machine'},
                                                    'time': {'$first': '$timestamp'}}}])
        return list(results)
