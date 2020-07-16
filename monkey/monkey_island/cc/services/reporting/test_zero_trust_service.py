import common.data.zero_trust_consts as zero_trust_consts
import monkey_island.cc.services.reporting.zero_trust_service
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.services.reporting.zero_trust_service import \
    ZeroTrustService
from monkey_island.cc.testing.IslandTestCase import IslandTestCase

EXPECTED_DICT = {
    zero_trust_consts.AUTOMATION_ORCHESTRATION: [],
    zero_trust_consts.DATA: [
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_DATA_TRANSIT],
            "status": zero_trust_consts.STATUS_FAILED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_FAILED,
                    "test": zero_trust_consts.TESTS_MAP
                    [zero_trust_consts.TEST_DATA_ENDPOINT_HTTP][zero_trust_consts.TEST_EXPLANATION_KEY]
                },
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP
                    [zero_trust_consts.TEST_DATA_ENDPOINT_ELASTIC][zero_trust_consts.TEST_EXPLANATION_KEY]
                },
            ]
        }
    ],
    zero_trust_consts.DEVICES: [
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_ENDPOINT_SECURITY],
            "status": zero_trust_consts.STATUS_FAILED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP
                    [zero_trust_consts.TEST_MACHINE_EXPLOITED][zero_trust_consts.TEST_EXPLANATION_KEY]
                },
                {
                    "status": zero_trust_consts.STATUS_FAILED,
                    "test": zero_trust_consts.TESTS_MAP
                    [zero_trust_consts.TEST_ENDPOINT_SECURITY_EXISTS][zero_trust_consts.TEST_EXPLANATION_KEY]
                },
            ]
        }
    ],
    zero_trust_consts.NETWORKS: [
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_SEGMENTATION],
            "status": zero_trust_consts.STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_SEGMENTATION][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_USER_BEHAVIOUR],
            "status": zero_trust_consts.STATUS_VERIFY,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_VERIFY,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_SCHEDULED_EXECUTION][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_USERS_MAC_POLICIES],
            "status": zero_trust_consts.STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_COMMUNICATE_AS_NEW_USER][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_ANALYZE_NETWORK_TRAFFIC],
            "status": zero_trust_consts.STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_MALICIOUS_ACTIVITY_TIMELINE][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_RESTRICTIVE_NETWORK_POLICIES],
            "status": zero_trust_consts.STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_TUNNELING][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        },
    ],
    zero_trust_consts.PEOPLE: [
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_USER_BEHAVIOUR],
            "status": zero_trust_consts.STATUS_VERIFY,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_VERIFY,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_SCHEDULED_EXECUTION][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_USERS_MAC_POLICIES],
            "status": zero_trust_consts.STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_COMMUNICATE_AS_NEW_USER][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        }
    ],
    zero_trust_consts.VISIBILITY_ANALYTICS: [
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_USERS_MAC_POLICIES],
            "status": zero_trust_consts.STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_COMMUNICATE_AS_NEW_USER][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_ANALYZE_NETWORK_TRAFFIC],
            "status": zero_trust_consts.STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_MALICIOUS_ACTIVITY_TIMELINE][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": zero_trust_consts.PRINCIPLES[zero_trust_consts.PRINCIPLE_RESTRICTIVE_NETWORK_POLICIES],
            "status": zero_trust_consts.STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": zero_trust_consts.STATUS_UNEXECUTED,
                    "test": zero_trust_consts.TESTS_MAP[zero_trust_consts.TEST_TUNNELING][
                        zero_trust_consts.TEST_EXPLANATION_KEY]
                }
            ]
        },
    ],
    zero_trust_consts.WORKLOADS: []
}


def save_example_findings():
    # arrange
    Finding.save_finding(zero_trust_consts.TEST_ENDPOINT_SECURITY_EXISTS, zero_trust_consts.STATUS_PASSED,
                         [])  # devices passed = 1
    Finding.save_finding(zero_trust_consts.TEST_ENDPOINT_SECURITY_EXISTS, zero_trust_consts.STATUS_PASSED,
                         [])  # devices passed = 2
    Finding.save_finding(zero_trust_consts.TEST_ENDPOINT_SECURITY_EXISTS, zero_trust_consts.STATUS_FAILED,
                         [])  # devices failed = 1
    # devices unexecuted = 1
    # people verify = 1
    # networks verify = 1
    Finding.save_finding(zero_trust_consts.TEST_SCHEDULED_EXECUTION, zero_trust_consts.STATUS_VERIFY, [])
    # people verify = 2
    # networks verify = 2
    Finding.save_finding(zero_trust_consts.TEST_SCHEDULED_EXECUTION, zero_trust_consts.STATUS_VERIFY, [])
    # data failed 1
    Finding.save_finding(zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_FAILED, [])
    # data failed 2
    Finding.save_finding(zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_FAILED, [])
    # data failed 3
    Finding.save_finding(zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_FAILED, [])
    # data failed 4
    Finding.save_finding(zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_FAILED, [])
    # data failed 5
    Finding.save_finding(zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_FAILED, [])
    # data verify 1
    Finding.save_finding(zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_VERIFY, [])
    # data verify 2
    Finding.save_finding(zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_VERIFY, [])
    # data passed 1
    Finding.save_finding(zero_trust_consts.TEST_DATA_ENDPOINT_HTTP, zero_trust_consts.STATUS_PASSED, [])


class TestZeroTrustService(IslandTestCase):
    def test_get_pillars_grades(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        save_example_findings()

        expected = [
            {
                zero_trust_consts.STATUS_FAILED: 5,
                zero_trust_consts.STATUS_VERIFY: 2,
                zero_trust_consts.STATUS_PASSED: 1,
                zero_trust_consts.STATUS_UNEXECUTED: 1,
                "pillar": "Data"
            },
            {
                zero_trust_consts.STATUS_FAILED: 0,
                zero_trust_consts.STATUS_VERIFY: 2,
                zero_trust_consts.STATUS_PASSED: 0,
                zero_trust_consts.STATUS_UNEXECUTED: 1,
                "pillar": "People"
            },
            {
                zero_trust_consts.STATUS_FAILED: 0,
                zero_trust_consts.STATUS_VERIFY: 2,
                zero_trust_consts.STATUS_PASSED: 0,
                zero_trust_consts.STATUS_UNEXECUTED: 4,
                "pillar": "Networks"
            },
            {
                zero_trust_consts.STATUS_FAILED: 1,
                zero_trust_consts.STATUS_VERIFY: 0,
                zero_trust_consts.STATUS_PASSED: 2,
                zero_trust_consts.STATUS_UNEXECUTED: 1,
                "pillar": "Devices"
            },
            {
                zero_trust_consts.STATUS_FAILED: 0,
                zero_trust_consts.STATUS_VERIFY: 0,
                zero_trust_consts.STATUS_PASSED: 0,
                zero_trust_consts.STATUS_UNEXECUTED: 0,
                "pillar": "Workloads"
            },
            {
                zero_trust_consts.STATUS_FAILED: 0,
                zero_trust_consts.STATUS_VERIFY: 0,
                zero_trust_consts.STATUS_PASSED: 0,
                zero_trust_consts.STATUS_UNEXECUTED: 3,
                "pillar": "Visibility & Analytics"
            },
            {
                zero_trust_consts.STATUS_FAILED: 0,
                zero_trust_consts.STATUS_VERIFY: 0,
                zero_trust_consts.STATUS_PASSED: 0,
                zero_trust_consts.STATUS_UNEXECUTED: 0,
                "pillar": "Automation & Orchestration"
            }
        ]

        result = ZeroTrustService.get_pillars_grades()

        self.assertEqual(result, expected)

    def test_get_principles_status(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        self.maxDiff = None

        save_example_findings()

        expected = dict(EXPECTED_DICT)  # new mutable

        result = ZeroTrustService.get_principles_status()
        # Compare expected and result, no order:
        for pillar_name, pillar_principles_status_result in result.items():
            for index, pillar_principle_status_expected in enumerate(expected.get(pillar_name)):
                correct_one = None
                for pillar_principle_status_result in pillar_principles_status_result:
                    if pillar_principle_status_result["principle"] == pillar_principle_status_expected["principle"]:
                        correct_one = pillar_principle_status_result
                        break

                # Compare tests no order
                self.assertTrue(compare_lists_no_order(correct_one["tests"], pillar_principle_status_expected["tests"]))
                # Compare the rest
                del pillar_principle_status_expected["tests"]
                del correct_one["tests"]
                self.assertEqual(sorted(correct_one), sorted(pillar_principle_status_expected))

    def test_get_pillars_to_statuses(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        self.maxDiff = None

        expected = {
            zero_trust_consts.AUTOMATION_ORCHESTRATION: zero_trust_consts.STATUS_UNEXECUTED,
            zero_trust_consts.DEVICES: zero_trust_consts.STATUS_UNEXECUTED,
            zero_trust_consts.NETWORKS: zero_trust_consts.STATUS_UNEXECUTED,
            zero_trust_consts.PEOPLE: zero_trust_consts.STATUS_UNEXECUTED,
            zero_trust_consts.VISIBILITY_ANALYTICS: zero_trust_consts.STATUS_UNEXECUTED,
            zero_trust_consts.WORKLOADS: zero_trust_consts.STATUS_UNEXECUTED,
            zero_trust_consts.DATA: zero_trust_consts.STATUS_UNEXECUTED
        }

        self.assertEqual(ZeroTrustService.get_pillars_to_statuses(), expected)

        save_example_findings()

        expected = {
            zero_trust_consts.AUTOMATION_ORCHESTRATION: zero_trust_consts.STATUS_UNEXECUTED,
            zero_trust_consts.DEVICES: zero_trust_consts.STATUS_FAILED,
            zero_trust_consts.NETWORKS: zero_trust_consts.STATUS_VERIFY,
            zero_trust_consts.PEOPLE: zero_trust_consts.STATUS_VERIFY,
            zero_trust_consts.VISIBILITY_ANALYTICS: zero_trust_consts.STATUS_UNEXECUTED,
            zero_trust_consts.WORKLOADS: zero_trust_consts.STATUS_UNEXECUTED,
            zero_trust_consts.DATA: zero_trust_consts.STATUS_FAILED
        }

        self.assertEqual(ZeroTrustService.get_pillars_to_statuses(), expected)

    def test_get_events_without_overlap(self):
        monkey_island.cc.services.reporting.zero_trust_service.EVENT_FETCH_CNT = 5
        self.assertListEqual([], ZeroTrustService._get_events_without_overlap(5, [1, 2, 3]))
        self.assertListEqual([3], ZeroTrustService._get_events_without_overlap(6, [1, 2, 3]))
        self.assertListEqual([1, 2, 3, 4, 5], ZeroTrustService._get_events_without_overlap(10, [1, 2, 3, 4, 5]))


def compare_lists_no_order(s, t):
    t = list(t)  # make a mutable copy
    try:
        for elem in s:
            t.remove(elem)
    except ValueError:
        return False
    return not t
