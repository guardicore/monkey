import os

from monkey_island.cc.server_utils import consts


def test_monkey_island_abs_path():
    assert consts.MONKEY_ISLAND_ABS_PATH.endswith("monkey_island")
    assert os.path.isdir(consts.MONKEY_ISLAND_ABS_PATH)
