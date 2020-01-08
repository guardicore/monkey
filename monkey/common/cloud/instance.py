from typing import List

from common.cloud.aws.aws_instance import AwsInstance
from common.cloud.azure.azure_instance import AzureInstance


class CloudInstance(object):
    def is_instance(self) -> bool:
        raise NotImplementedError()

    def get_cloud_provider_name(self) -> str:
        raise NotImplementedError()

    all_cloud_instances = [AwsInstance(), AzureInstance()]

    @staticmethod
    def get_all_cloud_instances() -> List['CloudInstance']:
        return CloudInstance.all_cloud_instances
