from common.cloud.scoutsuite.ScoutSuite.output.result_encoder import ScoutJsonEncoder
from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.telemetry.base_telem import BaseTelem


class ScoutSuiteTelem(BaseTelem):

    def __init__(self, data):
        """
        Default ScoutSuite telemetry constructor
        :param data: Data gathered via ScoutSuite (
        """
        super().__init__()
        self.data = data

    json_encoder = ScoutJsonEncoder
    telem_category = TelemCategoryEnum.SCOUTSUITE

    def get_data(self):
        return {
            'data': self.data
        }
