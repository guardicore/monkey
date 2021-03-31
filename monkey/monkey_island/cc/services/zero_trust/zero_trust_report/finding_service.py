from dataclasses import dataclass
from typing import List, Union

from bson import SON

from common.common_consts import zero_trust_consts
from common.utils.exceptions import UnknownFindingError
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding import MonkeyFinding
from monkey_island.cc.models.zero_trust.scoutsuite_finding import ScoutSuiteFinding
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_details_service import MonkeyZTDetailsService


@dataclass
class EnrichedFinding:
    finding_id: str
    test: str
    test_key: str
    pillars: List[str]
    status: str
    details: Union[dict, None]


class FindingService:

    @staticmethod
    def get_all_findings_from_db() -> List[Finding]:
        return list(Finding.objects)

    @staticmethod
    def get_all_findings_for_ui() -> List[EnrichedFinding]:
        findings = FindingService.get_all_findings_from_db()
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
            details=None
        )
        return enriched_finding

    @staticmethod
    def _get_finding_details(finding: Finding) -> Union[dict, SON]:
        if type(finding) == MonkeyFinding:
            return MonkeyZTDetailsService.fetch_details_for_display(finding.details.id)
        elif type(finding) == ScoutSuiteFinding:
            return finding.details.fetch().to_mongo()
        else:
            raise UnknownFindingError(f"Unknown finding type {str(type(finding))}")
