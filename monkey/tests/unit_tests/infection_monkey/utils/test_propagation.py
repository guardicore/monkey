from infection_monkey.utils.propagation import should_propagate


def test_should_propagate_current_less_than_max():
    maximum_depth = 2
    current_depth = 1

    assert should_propagate(maximum_depth, current_depth) is True


def test_should_propagate_current_greater_than_max():
    maximum_depth = 2
    current_depth = 3

    assert should_propagate(maximum_depth, current_depth) is False


def test_should_propagate_current_equal_to_max():
    maximum_depth = 2
    current_depth = maximum_depth

    assert should_propagate(maximum_depth, current_depth) is False
