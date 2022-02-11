from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.telemetry.base_telem import BaseTelem


class AwsInstanceTelemetry(BaseTelem):
    def __init__(self, aws_instance_info):
        """
        Default AWS instance telemetry constructor
        :param aws_instance_info: Aws Instance info
        """
        self.aws_instance_info = aws_instance_info

    telem_category = TelemCategoryEnum.AWS_INFO

    def get_data(self):
        return self.aws_instance_info

    def send(self, log_data=False):
        super(AwsInstanceTelemetry, self).send(log_data)
