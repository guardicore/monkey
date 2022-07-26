from functools import wraps
from typing import Callable

from common.utils.code_utils import freeze_lists_in_dict


def freeze_lists(function: Callable):
    @wraps(function)
    def wrapper(self, data, **kwargs):
        data = freeze_lists_in_dict(data)
        return function(self, data, **kwargs)

    return wrapper
