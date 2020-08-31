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
        @T1041.is_status_disabled
        def get_technique_status_and_data():
            monkeys = list(Monkey.objects())
            info = [{'src': monkey['command_control_channel']['src'],
                    'dst': monkey['command_control_channel']['dst']}
                    for monkey in monkeys if monkey['command_control_channel']]
            if info:
                status = ScanStatus.USED.value
            else:
                status = ScanStatus.UNSCANNED.value
            return (status, info)

        status, info = get_technique_status_and_data()

        data = T1041.get_base_data_by_status(status)
        data.update({'command_control_channel': info})
        return data
