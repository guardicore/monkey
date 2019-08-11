from itertools import chain, combinations


def power_set(iterable):
    """
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    s = list(iterable)
    return [list(x) for x in list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))]