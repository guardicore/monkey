from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.reporting.report import ReportService
from common.utils.attack_utils import ScanStatus
from common.data.post_breach_consts import POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION


__author__ = "shreyamalviya"


class T1156(AttackTechnique):
    tech_id = "T1156"
    unscanned_msg = "Monkey did not try modifying Linux's shell startup files on the system."
    scanned_msg = "Monkey tried modifying Linux's shell startup files on the system but failed."
    used_msg = "Monkey modified Linux's shell startup files on the system."

    @staticmethod
    def get_report_data():
        data = {'title': T1156.technique_title(), 'info': []}

        scanned_nodes = ReportService.get_scanned()
        status = ScanStatus.UNSCANNED.value

        for node in scanned_nodes:
            if node['pba_results'] != 'None':
                for pba in node['pba_results']:
                    if pba['name'] == POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION:
                        if 'powershell.exe' not in pba['command']:
                            status = ScanStatus.USED.value if pba['result'][1]\
                                                        else ScanStatus.SCANNED.value
                            data['info'].append({
                                    'machine': {
                                        'hostname': pba['hostname'],
                                        'ips': node['ip_addresses']
                                    },
                                    'result': pba['result'][0].replace('#', '')
                                })
            data.update(T1156.get_base_data_by_status(status))
        return data
