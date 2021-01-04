# abstract, static method decorator
# noinspection PyPep8Naming
import operator
from functools import reduce
from typing import List, Union, Any


class abstractstatic(staticmethod):
    __slots__ = ()

    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True

    __isabstractmethod__ = True


def get_dict_value_by_path(data: dict, path: List[str]) -> Any:
    return reduce(operator.getitem, path, data)
