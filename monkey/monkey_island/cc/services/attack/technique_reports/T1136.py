from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.reporting.report import ReportService
from common.utils.attack_utils import ScanStatus
from common.data.post_breach_consts import POST_BREACH_BACKDOOR_USER, POST_BREACH_COMMUNICATE_AS_NEW_USER

__author__ = "shreyamalviya"


class T1136(AttackTechnique):
    tech_id = "T1136"
    unscanned_msg = "Monkey didn't try creating a new user on the network's systems."
    scanned_msg = "Monkey tried creating a new user on the network's systems, but failed."
    used_msg = "Monkey created a new user on the network's systems."

    @staticmethod
    def get_report_data():
        data = {'title': T1136.technique_title()}

        scanned_nodes = ReportService.get_scanned()
        status = ScanStatus.UNSCANNED.value
        for node in scanned_nodes:
            if node['pba_results'] != 'None':
                for pba in node['pba_results']:
                    if pba['name'] in [POST_BREACH_BACKDOOR_USER,
                                       POST_BREACH_COMMUNICATE_AS_NEW_USER]:
                        status = ScanStatus.USED.value if pba['result'][1]\
                                                       else ScanStatus.SCANNED.value
                        data.update({
                            'info': [{
                                'machine': {
                                    'hostname': pba['hostname'],
                                    'ips': node['ip_addresses'],
                                },
                                'result': ': '.join([pba['name'], pba['result'][0]])
                            }]
                        })
            data.update(T1136.get_base_data_by_status(status))
        return data
