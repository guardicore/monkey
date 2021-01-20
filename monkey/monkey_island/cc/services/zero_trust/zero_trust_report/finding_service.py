from dataclasses import dataclass
from typing import List, Union

from bson import SON

from common.common_consts import zero_trust_consts
from common.utils.exceptions import UnknownFindingError
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_details_service import MonkeyZTDetailsService


@dataclass
class EnrichedFinding:
    finding_id: str
    test: str
    test_key: str
    pillars: List[str]
    status: str
    finding_type: str
    details: Union[dict, None]


class FindingService:

    @staticmethod
    def get_all_findings() -> List[EnrichedFinding]:
        findings = list(Finding.objects)
        for i in range(len(findings)):
            details = FindingService._get_finding_details(findings[i])
            findings[i] = findings[i].to_mongo()
            findings[i] = FindingService._get_enriched_finding(findings[i])
            findings[i].details = details
        return findings

    @staticmethod
    def _get_enriched_finding(finding: Finding) -> EnrichedFinding:
        test_info = zero_trust_consts.TESTS_MAP[finding['test']]
        enriched_finding = EnrichedFinding(
            finding_id=str(finding['_id']),
            test=test_info[zero_trust_consts.FINDING_EXPLANATION_BY_STATUS_KEY][finding['status']],
            test_key=finding['test'],
            pillars=test_info[zero_trust_consts.PILLARS_KEY],
            status=finding['status'],
            finding_type=finding['finding_type'],
            details=None
        )
        return enriched_finding

    @staticmethod
    def _get_finding_details(finding: Finding) -> Union[dict, SON]:
        if finding.finding_type == zero_trust_consts.MONKEY_FINDING:
            return MonkeyZTDetailsService.fetch_details_for_display(finding.details.id)
        elif finding.finding_type == zero_trust_consts.SCOUTSUITE_FINDING:
            return finding.details.fetch().to_mongo()
        else:
            raise UnknownFindingError(f"Unknown finding type {finding.finding_type}")
