from monkey_island.cc.services.reporting.zero_trust_service import ZeroTrustService

from common.data.zero_trust_consts import *
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


def save_example_findings():
    # arrange
    Finding.save_finding(TEST_ENDPOINT_SECURITY_EXISTS, STATUS_POSITIVE, [])  # devices positive = 1
    Finding.save_finding(TEST_ENDPOINT_SECURITY_EXISTS, STATUS_POSITIVE, [])  # devices positive = 2
    Finding.save_finding(TEST_ENDPOINT_SECURITY_EXISTS, STATUS_CONCLUSIVE, [])  # devices conclusive = 1
    # devices unexecuted = 1
    # people inconclusive = 1
    # networks inconclusive = 1
    Finding.save_finding(TEST_SCHEDULED_EXECUTION, STATUS_INCONCLUSIVE, [])
    # people inconclusive = 2
    # networks inconclusive = 2
    Finding.save_finding(TEST_SCHEDULED_EXECUTION, STATUS_INCONCLUSIVE, [])
    # data conclusive 1
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_CONCLUSIVE, [])
    # data conclusive 2
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_CONCLUSIVE, [])
    # data conclusive 3
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_CONCLUSIVE, [])
    # data conclusive 4
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_CONCLUSIVE, [])
    # data conclusive 5
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_CONCLUSIVE, [])
    # data inconclusive 1
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_INCONCLUSIVE, [])
    # data inconclusive 2
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_INCONCLUSIVE, [])
    # data positive 1
    Finding.save_finding(TEST_DATA_ENDPOINT_HTTP, STATUS_POSITIVE, [])


class TestZeroTrustService(IslandTestCase):
    def test_get_pillars_grades(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        save_example_findings()

        expected = [
            {
                "Conclusive": 5,
                "Inconclusive": 2,
                "Positive": 1,
                "Unexecuted": 1,
                "pillar": "Data"
            },
            {
                "Conclusive": 0,
                "Inconclusive": 2,
                "Positive": 0,
                "Unexecuted": 0,
                "pillar": "People"
            },
            {
                "Conclusive": 0,
                "Inconclusive": 2,
                "Positive": 0,
                "Unexecuted": 2,
                "pillar": "Networks"
            },
            {
                "Conclusive": 1,
                "Inconclusive": 0,
                "Positive": 2,
                "Unexecuted": 1,
                "pillar": "Devices"
            },
            {
                "Conclusive": 0,
                "Inconclusive": 0,
                "Positive": 0,
                "Unexecuted": 0,
                "pillar": "Workloads"
            },
            {
                "Conclusive": 0,
                "Inconclusive": 0,
                "Positive": 0,
                "Unexecuted": 1,
                "pillar": "Visibility & Analytics"
            },
            {
                "Conclusive": 0,
                "Inconclusive": 0,
                "Positive": 0,
                "Unexecuted": 0,
                "pillar": "Automation & Orchestration"
            }
        ]

        result = ZeroTrustService.get_pillars_grades()

        self.assertEquals(result, expected)

    def test_get_recommendations_status(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        save_example_findings()

        expected = {
            AUTOMATION_ORCHESTRATION: [],
            DATA: [
                {
                    "recommendation": RECOMMENDATIONS[RECOMMENDATION_DATA_TRANSIT],
                    "status": STATUS_CONCLUSIVE,
                    "tests": [
                        {
                            "status": STATUS_UNEXECUTED,
                            "test": TESTS_MAP[TEST_DATA_ENDPOINT_ELASTIC][TEST_EXPLANATION_KEY]
                        },
                        {
                            "status": STATUS_CONCLUSIVE,
                            "test": TESTS_MAP[TEST_DATA_ENDPOINT_HTTP][TEST_EXPLANATION_KEY]
                        }
                    ]
                }
            ],
            DEVICES: [
                {
                    "recommendation": RECOMMENDATIONS[RECOMMENDATION_ENDPOINT_SECURITY],
                    "status": STATUS_CONCLUSIVE,
                    "tests": [
                        {
                            "status": STATUS_CONCLUSIVE,
                            "test": TESTS_MAP[TEST_ENDPOINT_SECURITY_EXISTS][TEST_EXPLANATION_KEY]
                        },
                        {
                            "status": STATUS_UNEXECUTED,
                            "test": TESTS_MAP[TEST_MACHINE_EXPLOITED][TEST_EXPLANATION_KEY]
                        }
                    ]
                }
            ],
            NETWORKS: [
                {
                    "recommendation": RECOMMENDATIONS[RECOMMENDATION_SEGMENTATION],
                    "status": STATUS_UNEXECUTED,
                    "tests": [
                        {
                            "status": STATUS_UNEXECUTED,
                            "test": TESTS_MAP[TEST_SEGMENTATION][TEST_EXPLANATION_KEY]
                        }
                    ]
                },
                {
                    "recommendation": RECOMMENDATIONS[RECOMMENDATION_USER_BEHAVIOUR],
                    "status": STATUS_INCONCLUSIVE,
                    "tests": [
                        {
                            "status": STATUS_INCONCLUSIVE,
                            "test": TESTS_MAP[TEST_SCHEDULED_EXECUTION][TEST_EXPLANATION_KEY]
                        }
                    ]
                },
                {
                    "recommendation": RECOMMENDATIONS[RECOMMENDATION_ANALYZE_NETWORK_TRAFFIC],
                    "status": STATUS_UNEXECUTED,
                    "tests": [
                        {
                            "status": STATUS_UNEXECUTED,
                            "test": TESTS_MAP[TEST_MALICIOUS_ACTIVITY_TIMELINE][TEST_EXPLANATION_KEY]
                        }
                    ]
                }
            ],
            PEOPLE: [
                {
                    "recommendation": RECOMMENDATIONS[RECOMMENDATION_USER_BEHAVIOUR],
                    "status": STATUS_INCONCLUSIVE,
                    "tests": [
                        {
                            "status": STATUS_INCONCLUSIVE,
                            "test": TESTS_MAP[TEST_SCHEDULED_EXECUTION][TEST_EXPLANATION_KEY]
                        }
                    ]
                }
            ],
            "Visibility & Analytics": [
                {
                    "recommendation": RECOMMENDATIONS[RECOMMENDATION_ANALYZE_NETWORK_TRAFFIC],
                    "status": STATUS_UNEXECUTED,
                    "tests": [
                        {
                            "status": STATUS_UNEXECUTED,
                            "test": TESTS_MAP[TEST_MALICIOUS_ACTIVITY_TIMELINE][TEST_EXPLANATION_KEY]
                        }
                    ]
                }
            ],
            "Workloads": []
        }

        self.assertEquals(ZeroTrustService.get_recommendations_status(), expected)

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

        self.assertEquals(ZeroTrustService.get_pillars_to_statuses(), expected)

        save_example_findings()

        expected = {
            AUTOMATION_ORCHESTRATION: STATUS_UNEXECUTED,
            DEVICES: STATUS_CONCLUSIVE,
            NETWORKS: STATUS_INCONCLUSIVE,
            PEOPLE: STATUS_INCONCLUSIVE,
            VISIBILITY_ANALYTICS: STATUS_UNEXECUTED,
            WORKLOADS: STATUS_UNEXECUTED,
            DATA: STATUS_CONCLUSIVE
        }

        self.assertEquals(ZeroTrustService.get_pillars_to_statuses(), expected)
