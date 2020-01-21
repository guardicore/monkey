from common.cloud.environment_names import Environment


class CloudInstance(object):
    """
    This is an abstract class which represents a cloud instance.

    The current machine can be a cloud instance (for example EC2 instance or Azure VM).
    """
    def is_instance(self) -> bool:
        raise NotImplementedError()

    def get_cloud_provider_name(self) -> Environment:
        raise NotImplementedError()
