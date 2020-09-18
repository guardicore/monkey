from typing import List

from common.common_consts import zero_trust_consts
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.services.zero_trust.events_service import EventsService


class FindingService:

    @staticmethod
    def get_all_findings() -> List[Finding]:
        findings = list(Finding.objects)
        details = []
        for i in range(len(findings)):
            if findings[i].type == zero_trust_consts.MONKEY_FINDING:
                details = EventsService.fetch_events_for_display(findings[i].details.id)
            elif findings[i].type == zero_trust_consts.SCOUTSUITE_FINDING:
                details = findings[i].details.fetch().to_mongo()
            findings[i] = findings[i].to_mongo()
            findings[i] = FindingService.get_enriched_finding(findings[i])
            findings[i]['details'] = details
        return findings

    @staticmethod
    def get_enriched_finding(finding):
        test_info = zero_trust_consts.TESTS_MAP[finding['test']]
        enriched_finding = {
            'finding_id': str(finding['_id']),
            'test': test_info[zero_trust_consts.FINDING_EXPLANATION_BY_STATUS_KEY][finding['status']],
            'test_key': finding['test'],
            'pillars': test_info[zero_trust_consts.PILLARS_KEY],
            'status': finding['status'],
            'type': finding['type']
        }
        return enriched_finding
