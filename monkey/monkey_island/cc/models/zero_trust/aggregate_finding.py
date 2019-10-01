from common.data.zero_trust_consts import TEST_MALICIOUS_ACTIVITY_TIMELINE, STATUS_VERIFY
from monkey_island.cc.models.zero_trust.finding import Finding


class AggregateFinding(Finding):
    @staticmethod
    def create_or_add_to_existing(test, status, events):
        """
        Create a new finding or add the events to an existing one if it's the same (same meaning same status and same
        test).

        :raises: Assertion error if this is used when there's more then one finding which fits the query - this is not
        when this function should be used.
        """
        existing_findings = Finding.objects(test=test, status=status)
        assert (len(existing_findings) < 2), "More than one finding exists for {}:{}".format(test, status)

        if len(existing_findings) == 0:
            Finding.save_finding(test, status, events)
        else:
            # Now we know for sure this is the only one
            orig_finding = existing_findings[0]
            orig_finding.add_events(events)
            orig_finding.save()


def add_malicious_activity_to_timeline(events):
    AggregateFinding.create_or_add_to_existing(
        test=TEST_MALICIOUS_ACTIVITY_TIMELINE,
        status=STATUS_VERIFY,
        events=events
    )
