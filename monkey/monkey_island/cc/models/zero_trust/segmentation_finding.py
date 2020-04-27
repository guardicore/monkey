from mongoengine import StringField

import common.data.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.finding import Finding


def need_to_overwrite_status(saved_status, new_status):
    return (saved_status == zero_trust_consts.STATUS_PASSED) and (new_status == zero_trust_consts.STATUS_FAILED)


class SegmentationFinding(Finding):
    first_subnet = StringField()
    second_subnet = StringField()

    @staticmethod
    def create_or_add_to_existing_finding(subnets, status, segmentation_event):
        """
        Creates a segmentation finding. If a segmentation finding with the relevant subnets already exists, adds the
        event to the existing finding, and the "worst" status is chosen (i.e. if the existing one is "Failed" it will
        remain so).

        :param subnets: the 2 subnets of this finding.
        :param status: STATUS_PASSED or STATUS_FAILED
        :param segmentation_event: The specific event
        """
        assert len(subnets) == 2

        # Sort them so A -> B and B -> A segmentation findings will be the same one.
        subnets.sort()

        existing_findings = SegmentationFinding.objects(first_subnet=subnets[0], second_subnet=subnets[1])

        if len(existing_findings) == 0:
            # No finding exists - create.
            new_finding = SegmentationFinding(
                first_subnet=subnets[0],
                second_subnet=subnets[1],
                test=zero_trust_consts.TEST_SEGMENTATION,
                status=status,
                events=[segmentation_event]
            )
            new_finding.save()
        else:
            # A finding exists (should be one). Add the event to it.
            assert len(existing_findings) == 1
            existing_finding = existing_findings[0]
            existing_finding.events.append(segmentation_event)
            if need_to_overwrite_status(existing_finding.status, status):
                existing_finding.status = status
            existing_finding.save()
