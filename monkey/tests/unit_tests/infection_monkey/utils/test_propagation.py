from infection_monkey.utils.propagation import maximum_depth_reached


def test_maximum_depth_reached__current_less_than_max():
    maximum_depth = 2
    current_depth = 1

    assert maximum_depth_reached(maximum_depth, current_depth) is False


def test_maximum_depth_reached__current_greater_than_max():
    maximum_depth = 2
    current_depth = 3

    assert maximum_depth_reached(maximum_depth, current_depth) is True


def test_maximum_depth_reached__current_equal_to_max():
    maximum_depth = 2
    current_depth = maximum_depth

    assert maximum_depth_reached(maximum_depth, current_depth) is True
