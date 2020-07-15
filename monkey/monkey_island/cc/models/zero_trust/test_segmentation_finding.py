import common.data.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.segmentation_finding import \
    SegmentationFinding
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestSegmentationFinding(IslandTestCase):
    def test_create_or_add_to_existing_finding(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        first_segment = "1.1.1.0/24"
        second_segment = "2.2.2.0-2.2.2.254"
        third_segment = "3.3.3.3"
        event = Event.create_event("bla", "bla", zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK)

        SegmentationFinding.create_or_add_to_existing_finding(
            subnets=[first_segment, second_segment],
            status=zero_trust_consts.STATUS_FAILED,
            segmentation_event=event
        )

        self.assertEqual(len(SegmentationFinding.objects()), 1)
        self.assertEqual(len(SegmentationFinding.objects()[0].events), 1)

        SegmentationFinding.create_or_add_to_existing_finding(
            # !!! REVERSE ORDER
            subnets=[second_segment, first_segment],
            status=zero_trust_consts.STATUS_FAILED,
            segmentation_event=event
        )

        self.assertEqual(len(SegmentationFinding.objects()), 1)
        self.assertEqual(len(SegmentationFinding.objects()[0].events), 2)

        SegmentationFinding.create_or_add_to_existing_finding(
            # !!! REVERSE ORDER
            subnets=[first_segment, third_segment],
            status=zero_trust_consts.STATUS_FAILED,
            segmentation_event=event
        )

        self.assertEqual(len(SegmentationFinding.objects()), 2)

        SegmentationFinding.create_or_add_to_existing_finding(
            # !!! REVERSE ORDER
            subnets=[second_segment, third_segment],
            status=zero_trust_consts.STATUS_FAILED,
            segmentation_event=event
        )

        self.assertEqual(len(SegmentationFinding.objects()), 3)
