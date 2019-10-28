from common.data.zero_trust_consts import *
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.services.reporting.zero_trust_service import ZeroTrustService
from monkey_island.cc.testing.IslandTestCase import IslandTestCase

EXPECTED_DICT = {
    AUTOMATION_ORCHESTRATION: [],
    DATA: [
        {
            "principle": PRINCIPLES[PRINCIPLE_DATA_TRANSIT],
            "status": STATUS_FAILED,
            "tests": [
                {
                    "status": STATUS_FAILED,
                    "test": TESTS_MAP[TEST_DATA_ENDPOINT_HTTP][TEST_EXPLANATION_KEY]
                },
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_DATA_ENDPOINT_ELASTIC][TEST_EXPLANATION_KEY]
                },
            ]
        }
    ],
    DEVICES: [
        {
            "principle": PRINCIPLES[PRINCIPLE_ENDPOINT_SECURITY],
            "status": STATUS_FAILED,
            "tests": [
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_MACHINE_EXPLOITED][TEST_EXPLANATION_KEY]
                },
                {
                    "status": STATUS_FAILED,
                    "test": TESTS_MAP[TEST_ENDPOINT_SECURITY_EXISTS][TEST_EXPLANATION_KEY]
                },
            ]
        }
    ],
    NETWORKS: [
        {
            "principle": PRINCIPLES[PRINCIPLE_SEGMENTATION],
            "status": STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_SEGMENTATION][TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": PRINCIPLES[PRINCIPLE_USER_BEHAVIOUR],
            "status": STATUS_VERIFY,
            "tests": [
                {
                    "status": STATUS_VERIFY,
                    "test": TESTS_MAP[TEST_SCHEDULED_EXECUTION][TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": PRINCIPLES[PRINCIPLE_USERS_MAC_POLICIES],
            "status": STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_COMMUNICATE_AS_NEW_USER][TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": PRINCIPLES[PRINCIPLE_ANALYZE_NETWORK_TRAFFIC],
            "status": STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_MALICIOUS_ACTIVITY_TIMELINE][TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": PRINCIPLES[PRINCIPLE_RESTRICTIVE_NETWORK_POLICIES],
            "status": STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_TUNNELING][TEST_EXPLANATION_KEY]
                }
            ]
        },
    ],
    PEOPLE: [
        {
            "principle": PRINCIPLES[PRINCIPLE_USER_BEHAVIOUR],
            "status": STATUS_VERIFY,
            "tests": [
                {
                    "status": STATUS_VERIFY,
                    "test": TESTS_MAP[TEST_SCHEDULED_EXECUTION][TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": PRINCIPLES[PRINCIPLE_USERS_MAC_POLICIES],
            "status": STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_COMMUNICATE_AS_NEW_USER][TEST_EXPLANATION_KEY]
                }
            ]
        }
    ],
    VISIBILITY_ANALYTICS: [
        {
            "principle": PRINCIPLES[PRINCIPLE_USERS_MAC_POLICIES],
            "status": STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_COMMUNICATE_AS_NEW_USER][TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": PRINCIPLES[PRINCIPLE_ANALYZE_NETWORK_TRAFFIC],
            "status": STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_MALICIOUS_ACTIVITY_TIMELINE][TEST_EXPLANATION_KEY]
                }
            ]
        },
        {
            "principle": PRINCIPLES[PRINCIPLE_RESTRICTIVE_NETWORK_POLICIES],
            "status": STATUS_UNEXECUTED,
            "tests": [
                {
                    "status": STATUS_UNEXECUTED,
                    "test": TESTS_MAP[TEST_TUNNELING][TEST_EXPLANATION_KEY]
                }
            ]
        },
    ],
    WORKLOADS: []
}


def save_example_findings():
    # arrange
    Finding.save_finding(TEST_ENDPOINT_SECURITY_EXISTS, STATUS_PASSED, [])  # devices passed = 1
    Finding.save_finding(TEST_ENDPOINT_SECURITY_EXISTS, STATUS_PASSED, [])  # devices passed = 2
    Finding.save_finding(TEST_ENDPOINT_SECURITY_EXISTS, STATUS_FAILED, [])  # devices failed = 1
    # devices unexecuted = 1
    # people verify = 1
    # networks verify = 1
    Finding.save_finding(TEST_SCHEDULED_EXECUTION, STATUS_VERIFY, [])
    # people verify = 2
    # networks verify = 2
    Finding.save_finding(TEST_SCHEDULED_EXECUTION, STATUS_VERIFY, [])
    # data failed 1
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_FAILED, [])
    # data failed 2
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_FAILED, [])
    # data failed 3
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_FAILED, [])
    # data failed 4
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_FAILED, [])
    # data failed 5
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_FAILED, [])
    # data verify 1
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_VERIFY, [])
    # data verify 2
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_VERIFY, [])
    # data passed 1
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_PASSED, [])


class TestZeroTrustService(IslandTestCase):
    def test_get_pillars_grades(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        save_example_findings()

        expected = [
            {
                STATUS_FAILED: 5,
                STATUS_VERIFY: 2,
                STATUS_PASSED: 1,
                STATUS_UNEXECUTED: 1,
                "pillar": "Data"
            },
            {
                STATUS_FAILED: 0,
                STATUS_VERIFY: 2,
                STATUS_PASSED: 0,
                STATUS_UNEXECUTED: 1,
                "pillar": "People"
            },
            {
                STATUS_FAILED: 0,
                STATUS_VERIFY: 2,
                STATUS_PASSED: 0,
                STATUS_UNEXECUTED: 4,
                "pillar": "Networks"
            },
            {
                STATUS_FAILED: 1,
                STATUS_VERIFY: 0,
                STATUS_PASSED: 2,
                STATUS_UNEXECUTED: 1,
                "pillar": "Devices"
            },
            {
                STATUS_FAILED: 0,
                STATUS_VERIFY: 0,
                STATUS_PASSED: 0,
                STATUS_UNEXECUTED: 0,
                "pillar": "Workloads"
            },
            {
                STATUS_FAILED: 0,
                STATUS_VERIFY: 0,
                STATUS_PASSED: 0,
                STATUS_UNEXECUTED: 3,
                "pillar": "Visibility & Analytics"
            },
            {
                STATUS_FAILED: 0,
                STATUS_VERIFY: 0,
                STATUS_PASSED: 0,
                STATUS_UNEXECUTED: 0,
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
            AUTOMATION_ORCHESTRATION: STATUS_UNEXECUTED,
            DEVICES: STATUS_UNEXECUTED,
            NETWORKS: STATUS_UNEXECUTED,
            PEOPLE: STATUS_UNEXECUTED,
            VISIBILITY_ANALYTICS: STATUS_UNEXECUTED,
            WORKLOADS: STATUS_UNEXECUTED,
            DATA: STATUS_UNEXECUTED
        }

        self.assertEqual(ZeroTrustService.get_pillars_to_statuses(), expected)

        save_example_findings()

        expected = {
            AUTOMATION_ORCHESTRATION: STATUS_UNEXECUTED,
            DEVICES: STATUS_FAILED,
            NETWORKS: STATUS_VERIFY,
            PEOPLE: STATUS_VERIFY,
            VISIBILITY_ANALYTICS: STATUS_UNEXECUTED,
            WORKLOADS: STATUS_UNEXECUTED,
            DATA: STATUS_FAILED
        }

        self.assertEqual(ZeroTrustService.get_pillars_to_statuses(), expected)


def compare_lists_no_order(s, t):
    t = list(t)   # make a mutable copy
    try:
        for elem in s:
            t.remove(elem)
    except ValueError:
        return False
    return not t
