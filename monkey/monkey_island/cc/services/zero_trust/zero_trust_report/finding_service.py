from typing import List

from common.common_consts import zero_trust_consts
from common.utils.exceptions import UnknownFindingError
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_details_service import MonkeyZTDetailsService


class FindingService:

    @staticmethod
    def get_all_findings() -> List[Finding]:
        findings = list(Finding.objects)
        for i in range(len(findings)):
            if findings[i].finding_type == zero_trust_consts.MONKEY_FINDING:
                details = MonkeyZTDetailsService.fetch_details_for_display(findings[i].details.id)
            elif findings[i].finding_type == zero_trust_consts.SCOUTSUITE_FINDING:
                details = findings[i].details.fetch().to_mongo()
            else:
                raise UnknownFindingError(f"Unknown finding type {findings[i].finding_type}")
            findings[i] = findings[i].to_mongo()
            findings[i] = FindingService._get_enriched_finding(findings[i])
            findings[i]['details'] = details
        return findings

    @staticmethod
    def _get_enriched_finding(finding: Finding) -> dict:
        test_info = zero_trust_consts.TESTS_MAP[finding['test']]
        enriched_finding = {
            'finding_id': str(finding['_id']),
            'test': test_info[zero_trust_consts.FINDING_EXPLANATION_BY_STATUS_KEY][finding['status']],
            'test_key': finding['test'],
            'pillars': test_info[zero_trust_consts.PILLARS_KEY],
            'status': finding['status'],
            'finding_type': finding['finding_type']
        }
        return enriched_finding
