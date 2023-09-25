from .aws_instance import AWSInstance
from .aws_service import AWSService


def build() -> AWSService:
    return AWSService(AWSInstance())
