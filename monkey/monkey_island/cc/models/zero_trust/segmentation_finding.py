from mongoengine import StringField

from common.data.zero_trust_consts import TEST_SEGMENTATION, STATUS_CONCLUSIVE, STATUS_POSITIVE
from monkey_island.cc.models.zero_trust.finding import Finding


def need_to_overwrite_status(saved_status, new_status):
    return (saved_status == STATUS_POSITIVE) and (new_status == STATUS_CONCLUSIVE)


class SegmentationFinding(Finding):
    """
    trying to add conclusive:
    If the finding doesn't exist at all: create conclusive
    else:
        if positive, turn to conclusive
    add event

    trying to add positive:
    If the finding doesn't exist at all: create positive
    else: add event
    """
    first_subnet = StringField()
    second_subnet = StringField()

    @staticmethod
    def create_or_add_to_existing_finding(subnets, status, segmentation_event):
        assert len(subnets) == 2

        # Sort them so A -> B and B -> A segmentation findings will be the same one.
        subnets.sort()

        existing_findings = SegmentationFinding.objects(first_subnet=subnets[0], second_subnet=subnets[1])

        if len(existing_findings) == 0:
            # No finding exists - create.
            new_finding = SegmentationFinding(
                first_subnet=subnets[0],
                second_subnet=subnets[1],
                test=TEST_SEGMENTATION,
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
