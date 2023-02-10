def maximum_depth_reached(maximum_depth: int, current_depth: int) -> bool:
    """
    Return whether or not the current depth has eclipsed the maximum depth.
    Values are nonnegative. Depth should increase from zero.

    :param maximum_depth: The maximum depth.
    :param current_depth: The current depth.
    :return: True if the current depth has reached the maximum depth, otherwise False.
    """
    return current_depth >= maximum_depth
