from common.network.network_range import *
from common.network.segmentation_utils import get_ip_in_src_and_not_in_dst
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestSegmentationUtils(IslandTestCase):
    def test_get_ip_in_src_and_not_in_dst(self):
        self.fail_if_not_testing_env()
        source = CidrRange("1.1.1.0/24")
        target = CidrRange("2.2.2.0/24")
        self.assertIsNone(get_ip_in_src_and_not_in_dst(
            [text_type("2.2.2.2")], source, target
        ))
        self.assertIsNone(get_ip_in_src_and_not_in_dst(
            [text_type("3.3.3.3"), text_type("4.4.4.4")], source, target
        ))
        self.assertIsNotNone(get_ip_in_src_and_not_in_dst(
            [text_type("8.8.8.8"), text_type("1.1.1.1")], source, target
        ))
