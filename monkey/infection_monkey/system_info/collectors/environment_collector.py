from common.cloud.aws.aws_instance import AwsInstance
from common.cloud.azure.azure_instance import AzureInstance
from common.cloud.environment_names import ON_PREMISE, AZURE, AWS
from infection_monkey.system_info.system_info_collector import SystemInfoCollector


def get_monkey_environment():
    # Check if on any cloud env. Default is on prem.
    if AwsInstance().is_instance():
        env = AWS
    elif AzureInstance().is_instance():
        env = AZURE
    # TODO: elif GcpInstance().is_gcp_instance():
    else:
        env = ON_PREMISE
    return env


class EnvironmentCollector(SystemInfoCollector):
    def __init__(self):
        super(EnvironmentCollector, self).__init__(name="EnvironmentCollector")

    def collect(self) -> dict:
        return {"environment": get_monkey_environment()}
