from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.models.monkey import Monkey
from common.utils.attack_utils import ScanStatus

__author__ = "VakarisZ"


class T1041(AttackTechnique):

    tech_id = "T1041"
    unscanned_msg = "Monkey didn't exfiltrate any info trough command and control channel."
    scanned_msg = ""
    used_msg = "Monkey exfiltrated info trough command and control channel."

    @staticmethod
    def get_report_data():
        monkeys = list(Monkey.objects())
        info = [{'src': monkey['c2_info']['src'],
                 'dst': monkey['c2_info']['dst']}
                for monkey in monkeys if monkey['c2_info']]
        if info:
            status = ScanStatus.USED.value
        else:
            status = ScanStatus.UNSCANNED.value
        data = T1041.get_base_data_by_status(status)
        data.update({'c2_info': info})
        return data
