from common.utils.attack_utils import ScanStatus
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.attack.technique_reports import AttackTechnique


class T1016(AttackTechnique):
    tech_id = "T1016"
    relevant_systems = ["Linux", "Windows"]
    unscanned_msg = "Monkey didn't gather network configurations."
    scanned_msg = ""
    used_msg = "Monkey gathered network configurations on systems in the network."

    @staticmethod
    def get_report_data():
        def get_technique_status_and_data():
            network_info = T1016._get_network_info()
            used_info = [entry for entry in network_info if entry["info"][0]["used"]]
            status = ScanStatus.USED.value if used_info else ScanStatus.UNSCANNED.value
            return (status, network_info)

        status, network_info = get_technique_status_and_data()

        data = T1016.get_base_data_by_status(status)
        data.update({"network_info": network_info})
        return data

    @staticmethod
    def _get_network_info():
        network_info = []
        for monkey in Monkey.objects():
            entry = {"machine": {"hostname": monkey.hostname, "ips": monkey.ip_addresses}}
            info = [{"used": bool(monkey.networks), "name": "Network interface info"}]
            entry["info"] = info
            network_info.append(entry)

        return network_info
