from unittest import TestCase


class TestPower_set(TestCase):
    def test_power_set(self):
        before = ('a', 'b', 'c')
        after_expected = [
            ('a', ),
            ('b',),
            ('c',),
            ('a', 'b'),
            ('a', 'c'),
            ('b', 'c'),
            ('a', 'b', 'c'),
        ]

        from common.utils.itertools_extensions import power_set
        self.assertEquals(list(power_set(before)), after_expected)
