from common.utils.attack_utils import ScanStatus
from monkey_island.cc.models.monkey import Monkey
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1041(AttackTechnique):
    tech_id = "T1041"
    unscanned_msg = "Monkey didn't exfiltrate any info trough command and control channel."
    scanned_msg = ""
    used_msg = "Monkey exfiltrated info trough command and control channel."

    @staticmethod
    def get_report_data():
        info = []

        if not T1041.is_enabled_in_config():
            status = ScanStatus.DISABLED.value
        else:
            monkeys = list(Monkey.objects())
            info = [{'src': monkey['command_control_channel']['src'],
                    'dst': monkey['command_control_channel']['dst']}
                    for monkey in monkeys if monkey['command_control_channel']]
            if info:
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value

        data = T1041.get_base_data_by_status(status)
        data.update({'command_control_channel': info})
        return data
