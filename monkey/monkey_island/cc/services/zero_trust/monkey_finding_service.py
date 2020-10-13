from typing import List

from bson import ObjectId

from common.common_consts import zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails
from monkey_island.cc.models.zero_trust.subnet_pair import SubnetPair


class MonkeyFindingService:

    @staticmethod
    def create_or_add_to_existing(test, status, events, subnet_pairs=None):
        """
        Create a new finding or add the events to an existing one if it's the same (same meaning same status and same
        test).

        :raises: Assertion error if this is used when there's more then one finding which fits the query - this is not
        when this function should be used.
        """
        existing_findings = Finding.objects(test=test, status=status)
        assert (len(existing_findings) < 2), "More than one finding exists for {}:{}".format(test, status)

        if len(existing_findings) == 0:
            MonkeyFindingService.create_new_finding(test, status, events, subnet_pairs)
        else:
            # Now we know for sure this is the only one
            MonkeyFindingService.add_events(existing_findings[0], events)
            if subnet_pairs:
                MonkeyFindingService.add_subnet_pairs(existing_findings[0], subnet_pairs)

    @staticmethod
    def create_new_finding(test: str, status: str, events: List[Event], subnet_pairs: List[SubnetPair]):
        details = MonkeyFindingDetails()
        details.events = events
        details.subnet_pairs = subnet_pairs
        details.save()
        Finding.save_finding(test, status, details)

    @staticmethod
    def add_events(finding: Finding, events: List[Event]):
        finding.details.fetch().add_events(events).save()

    @staticmethod
    def add_subnet_pairs(finding: Finding, subnet_pairs: List[List[str]]):
        finding_details = finding.details.fetch()
        for subnet_pair in subnet_pairs:
            subnet_pair_document = SubnetPair.create_subnet_pair(subnet_pair)
            if not MonkeyFindingService.is_subnet_pair_in_finding(finding, subnet_pair_document):
                finding_details.add_checked_subnet_pair(subnet_pair_document)
        finding_details.save()

    @staticmethod
    def is_subnet_pair_in_finding(finding: Finding, subnet_pair: SubnetPair):
        details = finding.details.fetch()
        return details.is_with_subnet_pair(subnet_pair)

    @staticmethod
    def get_events_by_finding(finding_id: str) -> List[object]:
        finding = Finding.objects.get(id=finding_id)
        pipeline = [{'$match': {'_id': ObjectId(finding.details.id)}},
                    {'$unwind': '$events'},
                    {'$project': {'events': '$events'}},
                    {'$replaceRoot': {'newRoot': '$events'}}]
        return list(MonkeyFindingDetails.objects.aggregate(*pipeline))

    @staticmethod
    def add_malicious_activity_to_timeline(events):
        MonkeyFindingService.create_or_add_to_existing(test=zero_trust_consts.TEST_MALICIOUS_ACTIVITY_TIMELINE,
                                                       status=zero_trust_consts.STATUS_VERIFY, events=events)
