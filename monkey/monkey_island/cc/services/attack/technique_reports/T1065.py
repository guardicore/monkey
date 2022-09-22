from typing import Iterable

from common.network.network_utils import address_to_ip_port
from common.utils.attack_utils import ScanStatus
from monkey_island.cc.models.telemetries.telemetry import Telemetry
from monkey_island.cc.server_utils.consts import ISLAND_PORT
from monkey_island.cc.services.attack.technique_reports import AttackTechnique


class T1065(AttackTechnique):
    tech_id = "T1065"
    relevant_systems = ["Linux", "Windows"]
    unscanned_msg = ""
    scanned_msg = ""
    used_msg = ""
    message = "Monkey used ports %s to communicate to C2 server."

    @staticmethod
    def get_report_data():
        non_standard_ports = [*T1065.get_tunnel_ports(), str(ISLAND_PORT)]
        T1065.used_msg = T1065.message % ", ".join(non_standard_ports)
        return T1065.get_base_data_by_status(ScanStatus.USED.value)

    @staticmethod
    def get_tunnel_ports() -> Iterable[str]:
        telems = Telemetry.objects(telem_category="tunnel", data__proxy__ne=None)
        return filter(None, [address_to_ip_port(telem["data"]["proxy"])[1] for telem in telems])
