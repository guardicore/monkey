from infection_monkey.utils.propagation import should_propagate


def get_config(max_depth):
    return {"config": {"depth": max_depth}}


def test_should_propagate_current_less_than_max():
    max_depth = 2
    current_depth = 1

    config = get_config(max_depth)

    assert should_propagate(config, current_depth) is True


def test_should_propagate_current_greater_than_max():
    max_depth = 2
    current_depth = 3

    config = get_config(max_depth)

    assert should_propagate(config, current_depth) is False


def test_should_propagate_current_equal_to_max():
    max_depth = 2
    current_depth = max_depth

    config = get_config(max_depth)

    assert should_propagate(config, current_depth) is False
