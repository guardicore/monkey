from typing import Mapping

from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.telemetry.base_telem import BaseTelem


class TunnelTelem(BaseTelem):
    def __init__(self, proxy: Mapping[str, str]):
        """
        Default tunnel telemetry constructor
        """
        super(TunnelTelem, self).__init__()
        self.proxy = proxy.get("https")

    telem_category = TelemCategoryEnum.TUNNEL

    def get_data(self):
        return {"proxy": self.proxy}
