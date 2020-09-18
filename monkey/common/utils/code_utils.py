# abstract, static method decorator
# noinspection PyPep8Naming
import operator
from functools import reduce
from typing import List


class abstractstatic(staticmethod):
    __slots__ = ()

    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True

    __isabstractmethod__ = True


def _get_value_by_path(data, path: List[str]):
    return reduce(operator.getitem, path, data)


def get_object_value_by_path(data_object: object, path: List[str]):
    return _get_value_by_path(data_object, path)


def get_dict_value_by_path(data_dict: dict, path: List[str]):
    return _get_value_by_path(data_dict, path)
