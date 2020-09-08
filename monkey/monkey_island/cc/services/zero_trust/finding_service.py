from typing import List

from common.common_consts import zero_trust_consts
from monkey_island.cc.models.zero_trust.finding import Finding


class FindingService:

    @staticmethod
    def get_all_findings() -> List[Finding]:
        return list(Finding.objects)

    @staticmethod
    def get_enriched_finding(finding):
        test_info = zero_trust_consts.TESTS_MAP[finding['test']]
        enriched_finding = {
            'finding_id': str(finding['_id']),
            'test': test_info[zero_trust_consts.FINDING_EXPLANATION_BY_STATUS_KEY][finding['status']],
            'test_key': finding['test'],
            'pillars': test_info[zero_trust_consts.PILLARS_KEY],
            'status': finding['status'],
        }
        return enriched_finding
