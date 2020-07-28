from common.utils.attack_utils import ScanStatus
from monkey_island.cc.models.monkey import Monkey
from monkey_island.cc.services.attack.technique_reports import AttackTechnique

__author__ = "VakarisZ"


class T1188(AttackTechnique):
    tech_id = "T1188"
    unscanned_msg = "Monkey didn't use multi-hop proxy."
    scanned_msg = ""
    used_msg = "Monkey used multi-hop proxy."

    @staticmethod
    def get_report_data():
        hops = []

        if not T1188.is_enabled_in_config():
            status = ScanStatus.DISABLED.value
        else:
            monkeys = Monkey.get_tunneled_monkeys()
            hops = []
            for monkey in monkeys:
                proxy_count = 0
                proxy = initial = monkey
                while proxy.tunnel:
                    proxy_count += 1
                    proxy = proxy.tunnel
                if proxy_count > 1:
                    hops.append({'from': initial.get_network_info(),
                                 'to': proxy.get_network_info(),
                                 'count': proxy_count})
            status = ScanStatus.USED.value if hops else ScanStatus.UNSCANNED.value

        data = T1188.get_base_data_by_status(status)
        data.update({'hops': hops})
        return data
