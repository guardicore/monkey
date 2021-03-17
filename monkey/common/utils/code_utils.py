# abstract, static method decorator
# noinspection PyPep8Naming
from typing import List


class abstractstatic(staticmethod):
    __slots__ = ()

    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True

    __isabstractmethod__ = True


def get_value_from_dict(dict_data: dict, path: List[str]):
    current_data = dict_data
    for key in path:
        current_data = current_data[key]
    return current_data
