from ophidian import DIContainer

from .aws_service import AWSService


def build(container: DIContainer) -> AWSService:
    return container.resolve(AWSService)
