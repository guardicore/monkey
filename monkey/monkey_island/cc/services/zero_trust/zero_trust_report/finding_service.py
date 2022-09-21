from dataclasses import dataclass
from typing import Dict, List, Union, cast

from bson import SON

from common.common_consts import zero_trust_consts
from common.utils.exceptions import UnknownFindingError
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding import MonkeyFinding
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_details_service import (
    MonkeyZTDetailsService,
)


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
        enriched_findings: List[EnrichedFinding] = []
        for finding in findings:
            finding_data = finding.to_mongo()
            enriched_finding = FindingService._get_enriched_finding(finding_data)
            details = FindingService._get_finding_details(finding)
            enriched_finding.details = details
            enriched_findings.append(enriched_finding)

        return enriched_findings

    @staticmethod
    def _get_enriched_finding(finding: SON) -> EnrichedFinding:
        test_info = zero_trust_consts.TESTS_MAP[finding["test"]]
        enriched_finding = EnrichedFinding(
            finding_id=str(finding["_id"]),
            test=cast(
                Dict[str, str], test_info[zero_trust_consts.FINDING_EXPLANATION_BY_STATUS_KEY]
            )[finding["status"]],
            test_key=finding["test"],
            pillars=cast(List[str], test_info[zero_trust_consts.PILLARS_KEY]),
            status=finding["status"],
            details=None,
        )
        return enriched_finding

    @staticmethod
    def _get_finding_details(finding: Finding) -> Union[dict, SON]:
        if type(finding) == MonkeyFinding:
            return MonkeyZTDetailsService.fetch_details_for_display(finding.details.id)
        else:
            raise UnknownFindingError(f"Unknown finding type {str(type(finding))}")
