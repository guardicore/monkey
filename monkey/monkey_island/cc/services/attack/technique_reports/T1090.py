from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.models import Monkey

__author__ = "VakarisZ"


class T1090(AttackTechnique):

    tech_id = "T1090"
    unscanned_msg = "Monkey didn't use connection proxy."
    scanned_msg = ""
    used_msg = "Monkey used connection proxy to communicate with machines on the network."

    @staticmethod
    def get_report_data():
        monkeys = Monkey.get_tunneled_monkeys()
        monkeys = [monkey.get_network_info() for monkey in monkeys]
        status = ScanStatus.USED.value if monkeys else ScanStatus.UNSCANNED.value
        data = T1090.get_base_data_by_status(status)
        data.update({'proxies': monkeys})
        return data


