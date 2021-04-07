from ScoutSuite.output.result_encoder import ScoutJsonEncoder
from ScoutSuite.providers.base.provider import BaseProvider

from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.telemetry.base_telem import BaseTelem


class ScoutSuiteTelem(BaseTelem):
    def __init__(self, provider: BaseProvider):
        super().__init__()
        self.provider_data = provider

    json_encoder = ScoutJsonEncoder
    telem_category = TelemCategoryEnum.SCOUTSUITE

    def get_data(self):
        return {"data":self.provider_data}
