from typing import List

import pytest
from tests.unit_tests.monkey_island.cc.services.zero_trust.test_common.example_finding_data import (  # noqa: E501
    save_example_findings,
)

from common.common_consts import zero_trust_consts
from common.common_consts.zero_trust_consts import (
    AUTOMATION_ORCHESTRATION,
    DATA,
    DEVICES,
    NETWORKS,
    PEOPLE,
    VISIBILITY_ANALYTICS,
    WORKLOADS,
)
from monkey_island.cc.services.zero_trust.zero_trust_report.pillar_service import PillarService


@pytest.mark.usefixtures("uses_database")
def test_get_pillars_grades():
    save_example_findings()
    expected_grades = _get_expected_pillar_grades()
    computed_grades = PillarService._get_pillars_grades()
    assert expected_grades == computed_grades


def _get_expected_pillar_grades() -> List[dict]:
    return [
        {
            zero_trust_consts.STATUS_FAILED: 3,
            zero_trust_consts.STATUS_VERIFY: 2,
            zero_trust_consts.STATUS_PASSED: 0,
            # 1 test of DATA pillar was executed in save_example_findings()
            zero_trust_consts.STATUS_UNEXECUTED: _get_cnt_of_tests_in_pillar(DATA) - 1,
            "pillar": "Data",
        },
        {
            zero_trust_consts.STATUS_FAILED: 0,
            zero_trust_consts.STATUS_VERIFY: 1,
            zero_trust_consts.STATUS_PASSED: 0,
            # 1 test of PEOPLE pillar was executed in save_example_findings()
            zero_trust_consts.STATUS_UNEXECUTED: _get_cnt_of_tests_in_pillar(PEOPLE) - 1,
            "pillar": "People",
        },
        {
            zero_trust_consts.STATUS_FAILED: 0,
            zero_trust_consts.STATUS_VERIFY: 1,
            zero_trust_consts.STATUS_PASSED: 0,
            # 1 test of NETWORKS pillar was executed in save_example_findings()
            zero_trust_consts.STATUS_UNEXECUTED: _get_cnt_of_tests_in_pillar(NETWORKS) - 1,
            "pillar": "Networks",
        },
        {
            zero_trust_consts.STATUS_FAILED: 1,
            zero_trust_consts.STATUS_VERIFY: 0,
            zero_trust_consts.STATUS_PASSED: 0,
            # 1 test of DEVICES pillar was executed in save_example_findings()
            zero_trust_consts.STATUS_UNEXECUTED: _get_cnt_of_tests_in_pillar(DEVICES) - 1,
            "pillar": "Devices",
        },
        {
            zero_trust_consts.STATUS_FAILED: 0,
            zero_trust_consts.STATUS_VERIFY: 0,
            zero_trust_consts.STATUS_PASSED: 0,
            # 0 tests of WORKLOADS pillar were executed in save_example_findings()
            zero_trust_consts.STATUS_UNEXECUTED: _get_cnt_of_tests_in_pillar(WORKLOADS),
            "pillar": "Workloads",
        },
        {
            zero_trust_consts.STATUS_FAILED: 0,
            zero_trust_consts.STATUS_VERIFY: 0,
            zero_trust_consts.STATUS_PASSED: 0,
            # 0 tests of VISIBILITY_ANALYTICS pillar were executed in save_example_findings()
            zero_trust_consts.STATUS_UNEXECUTED: _get_cnt_of_tests_in_pillar(VISIBILITY_ANALYTICS),
            "pillar": "Visibility & Analytics",
        },
        {
            zero_trust_consts.STATUS_FAILED: 0,
            zero_trust_consts.STATUS_VERIFY: 0,
            zero_trust_consts.STATUS_PASSED: 0,
            # 0 tests of AUTOMATION_ORCHESTRATION pillar were executed in save_example_findings()
            zero_trust_consts.STATUS_UNEXECUTED: _get_cnt_of_tests_in_pillar(
                AUTOMATION_ORCHESTRATION
            ),
            "pillar": "Automation & Orchestration",
        },
    ]


def _get_cnt_of_tests_in_pillar(pillar: str):
    tests_in_pillar = [
        value for (key, value) in zero_trust_consts.TESTS_MAP.items() if pillar in value["pillars"]
    ]
    return len(tests_in_pillar)


@pytest.mark.usefixtures("uses_database")
def test_get_pillars_to_statuses():
    # Test empty database
    expected = {
        zero_trust_consts.AUTOMATION_ORCHESTRATION: zero_trust_consts.STATUS_UNEXECUTED,
        zero_trust_consts.DEVICES: zero_trust_consts.STATUS_UNEXECUTED,
        zero_trust_consts.NETWORKS: zero_trust_consts.STATUS_UNEXECUTED,
        zero_trust_consts.PEOPLE: zero_trust_consts.STATUS_UNEXECUTED,
        zero_trust_consts.VISIBILITY_ANALYTICS: zero_trust_consts.STATUS_UNEXECUTED,
        zero_trust_consts.WORKLOADS: zero_trust_consts.STATUS_UNEXECUTED,
        zero_trust_consts.DATA: zero_trust_consts.STATUS_UNEXECUTED,
    }
    assert PillarService._get_pillars_to_statuses() == expected

    # Test with example finding set
    save_example_findings()
    expected = {
        zero_trust_consts.AUTOMATION_ORCHESTRATION: zero_trust_consts.STATUS_UNEXECUTED,
        zero_trust_consts.DEVICES: zero_trust_consts.STATUS_FAILED,
        zero_trust_consts.NETWORKS: zero_trust_consts.STATUS_VERIFY,
        zero_trust_consts.PEOPLE: zero_trust_consts.STATUS_VERIFY,
        zero_trust_consts.VISIBILITY_ANALYTICS: zero_trust_consts.STATUS_UNEXECUTED,
        zero_trust_consts.WORKLOADS: zero_trust_consts.STATUS_UNEXECUTED,
        zero_trust_consts.DATA: zero_trust_consts.STATUS_FAILED,
    }
    assert PillarService._get_pillars_to_statuses() == expected
