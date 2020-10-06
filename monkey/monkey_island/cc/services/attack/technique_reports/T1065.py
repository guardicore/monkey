from common.utils.attack_utils import ScanStatus
from monkey_island.cc.services.attack.technique_reports import AttackTechnique
from monkey_island.cc.services.config import ConfigService

__author__ = "VakarisZ"

from monkey_island.cc.services.config_schema.config_value_paths import CURRENT_SERVER_PATH


class T1065(AttackTechnique):
    tech_id = "T1065"
    unscanned_msg = ""
    scanned_msg = ""
    used_msg = ""
    message = "Monkey used port %s to communicate to C2 server."

    @staticmethod
    def get_report_data():
        port = ConfigService.get_config_value(CURRENT_SERVER_PATH).split(':')[1]
        T1065.used_msg = T1065.message % port
        return T1065.get_base_data_by_status(ScanStatus.USED.value)
