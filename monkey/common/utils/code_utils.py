import queue
from collections.abc import MutableSequence
from typing import Any, Dict, List, MutableMapping, Type, TypeVar

T = TypeVar("T")


class abstractstatic(staticmethod):
    __slots__ = ()

    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True

    __isabstractmethod__ = True


class Singleton(type):
    _instances: Dict[Type, type] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def queue_to_list(q: queue.Queue) -> List[Any]:
    list_ = []
    try:
        while True:
            list_.append(q.get_nowait())
    except queue.Empty:
        pass

    return list_


def del_key(mapping: MutableMapping[T, Any], key: T):
    """
    Delete a key from a mapping.

    Unlike the `del` keyword, this function does not raise a KeyError
    if the key does not exist.

    :param mapping: A mapping from which a key will be deleted
    :param key: A key to delete from `mapping`
    """
    try:
        del mapping[key]
    except KeyError:
        pass


def freeze_lists_in_mapping(mapping: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
    for key, value in mapping.items():
        if isinstance(value, MutableSequence):
            mapping[key] = tuple(value)
    return mapping
