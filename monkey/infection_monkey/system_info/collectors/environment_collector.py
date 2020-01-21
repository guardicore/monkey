from common.cloud.all_instances import get_all_cloud_instances
from common.cloud.environment_names import ON_PREMISE
from common.data.system_info_collectors_names import ENVIRONMENT_COLLECTOR
from infection_monkey.system_info.system_info_collector import SystemInfoCollector


def get_monkey_environment() -> str:
    env = ON_PREMISE
    for instance in get_all_cloud_instances():
        if instance.is_instance():
            env = instance.get_cloud_provider_name()
    return env


class EnvironmentCollector(SystemInfoCollector):
    def __init__(self):
        super().__init__(name=ENVIRONMENT_COLLECTOR)

    def collect(self) -> dict:
        return {"environment": get_monkey_environment()}
