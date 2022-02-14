from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.telemetry.base_telem import BaseTelem


class AWSInstanceTelemetry(BaseTelem):
    def __init__(self, aws_instance_id: str):
        """
        Default AWS instance telemetry constructor
        """
        self.aws_instance_info = {"instance_id": aws_instance_id}

    telem_category = TelemCategoryEnum.AWS_INFO

    def get_data(self):
        return self.aws_instance_info

    def send(self, log_data=False):
        super(AWSInstanceTelemetry, self).send(log_data)
