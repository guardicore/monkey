import unittest

from common.utils.code_utils import get_dict_value_by_path


class TestCodeUtils(unittest.TestCase):
    def test_get_dict_value_by_path(self):
        dict_for_test = {'a': {'b': {'c': 'result'}}}
        self.assertEqual(get_dict_value_by_path(dict_for_test, ['a', 'b', 'c']), 'result')
