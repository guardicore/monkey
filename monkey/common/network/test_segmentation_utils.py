from common.network.network_range import CidrRange
from common.network.segmentation_utils import get_ip_in_src_and_not_in_dst


class TestSegmentationUtils:
    def test_get_ip_in_src_and_not_in_dst(self):
        source = CidrRange("1.1.1.0/24")
        target = CidrRange("2.2.2.0/24")

        # IP not in both
        assert get_ip_in_src_and_not_in_dst(
            ["3.3.3.3", "4.4.4.4"], source, target
        ) is None

        # IP not in source, in target
        assert (get_ip_in_src_and_not_in_dst(
            ["2.2.2.2"], source, target
        )) is None

        # IP in source, not in target
        assert (get_ip_in_src_and_not_in_dst(
            ["8.8.8.8", "1.1.1.1"], source, target
        ))

        # IP in both subnets
        assert (get_ip_in_src_and_not_in_dst(
            ["8.8.8.8", "1.1.1.1"], source, source
        )) is None
