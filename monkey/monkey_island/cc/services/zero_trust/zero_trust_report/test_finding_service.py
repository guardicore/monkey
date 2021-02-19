from unittest.mock import MagicMock

import pytest

from common.common_consts.zero_trust_consts import TESTS_MAP, TEST_SCOUTSUITE_SERVICE_SECURITY, STATUS_FAILED, \
    DEVICES, NETWORKS, STATUS_PASSED, TEST_ENDPOINT_SECURITY_EXISTS
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_details_service import MonkeyZTDetailsService
from monkey_island.cc.services.zero_trust.test_common.finding_data import get_scoutsuite_finding_dto, \
    get_monkey_finding_dto
from monkey_island.cc.services.zero_trust.zero_trust_report.finding_service import FindingService, EnrichedFinding
from monkey_island.cc.test_common.fixtures.fixture_enum import FixtureEnum


@pytest.mark.usefixtures(FixtureEnum.USES_DATABASE)
def test_get_all_findings():
    get_scoutsuite_finding_dto().save()
    get_monkey_finding_dto().save()

    # This method fails due to mongomock not being able to simulate $unset, so don't test details
    MonkeyZTDetailsService.fetch_details_for_display = MagicMock(return_value=None)

    findings = FindingService.get_all_findings_for_ui()

    description = TESTS_MAP[TEST_SCOUTSUITE_SERVICE_SECURITY]['finding_explanation'][STATUS_FAILED]
    expected_finding0 = EnrichedFinding(finding_id=findings[0].finding_id,
                                        pillars=[DEVICES, NETWORKS],
                                        status=STATUS_FAILED,
                                        test=description,
                                        test_key=TEST_SCOUTSUITE_SERVICE_SECURITY,
                                        details=None)

    description = TESTS_MAP[TEST_ENDPOINT_SECURITY_EXISTS]['finding_explanation'][STATUS_PASSED]
    expected_finding1 = EnrichedFinding(finding_id=findings[1].finding_id,
                                        pillars=[DEVICES],
                                        status=STATUS_PASSED,
                                        test=description,
                                        test_key=TEST_ENDPOINT_SECURITY_EXISTS,
                                        details=None)

    # Don't test details
    details = []
    for finding in findings:
        details.append(finding.details)
        finding.details = None

    assert findings[0] == expected_finding0
    assert findings[1] == expected_finding1
