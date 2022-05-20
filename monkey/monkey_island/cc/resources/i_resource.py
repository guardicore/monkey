from abc import ABCMeta, abstractmethod
from typing import Sequence

from flask.views import MethodViewType


# Flask resources inherit from flask_restful.Resource, so custom interface
# must implement both metaclasses
class AbstractResource(ABCMeta, MethodViewType):
    pass


class IResource(metaclass=AbstractResource):
    @property
    @abstractmethod
    def urls(self) -> Sequence[str]:
        pass
