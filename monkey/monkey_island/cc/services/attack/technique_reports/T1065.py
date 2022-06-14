from common.utils.attack_utils import ScanStatus
from monkey_island.cc.models.monkey import Monkey
from monkey_island.cc.server_utils.consts import ISLAND_PORT
from monkey_island.cc.services.attack.technique_reports import AttackTechnique


class T1065(AttackTechnique):
    tech_id = "T1065"
    relevant_systems = ["Linux", "Windows"]
    unscanned_msg = ""
    scanned_msg = ""
    used_msg = ""
    message = "Monkey used port %s to communicate to C2 server."

    @staticmethod
    def get_report_data():
        monkey = Monkey.objects.first()
        tunnel = monkey.get_tunnel_info()["tunnel"]
        port = tunnel.split(":")[1] if tunnel is not None else ISLAND_PORT

        T1065.used_msg = T1065.message % port
        return T1065.get_base_data_by_status(ScanStatus.USED.value)
