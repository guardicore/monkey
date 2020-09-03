from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.telemetry.base_telem import BaseTelem

__author__ = "itay.mizeretz"


class SystemInfoTelem(BaseTelem):

    def __init__(self, system_info):
        """
        Default system info telemetry constructor
        :param system_info: System info returned from SystemInfoCollector.get_info()
        """
        super(SystemInfoTelem, self).__init__()
        self.system_info = system_info

    telem_category = TelemCategoryEnum.SYSTEM_INFO

    def get_data(self):
        return self.system_info

    def send(self, log_data=False):
        super(SystemInfoTelem, self).send(log_data)
