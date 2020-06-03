from common.network.network_range import CidrRange
from common.network.segmentation_utils import get_ip_in_src_and_not_in_dst
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestSegmentationUtils(IslandTestCase):
    def test_get_ip_in_src_and_not_in_dst(self):
        self.fail_if_not_testing_env()
        source = CidrRange("1.1.1.0/24")
        target = CidrRange("2.2.2.0/24")

        # IP not in both
        self.assertIsNone(get_ip_in_src_and_not_in_dst(
            ["3.3.3.3", "4.4.4.4"], source, target
        ))

        # IP not in source, in target
        self.assertIsNone(get_ip_in_src_and_not_in_dst(
            ["2.2.2.2"], source, target
        ))

        # IP in source, not in target
        self.assertIsNotNone(get_ip_in_src_and_not_in_dst(
            ["8.8.8.8", "1.1.1.1"], source, target
        ))

        # IP in both subnets
        self.assertIsNone(get_ip_in_src_and_not_in_dst(
            ["8.8.8.8", "1.1.1.1"], source, source
        ))
