from monkey_island.cc.services.reporting.zero_trust_service import ZeroTrustService

from common.data.zero_trust_consts import *
from monkey_island.cc.models.finding import Finding
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

    def test_get_directives_status(self):
        self.fail_if_not_testing_env()
        self.clean_finding_db()

        save_example_findings()

        expected = {
            AUTOMATION_ORCHESTRATION: [],
            DATA: [
                {
                    "directive": DIRECTIVE_DATA_TRANSIT,
                    "status": STATUS_CONCLUSIVE,
                    "tests": [
                        {
                            "status": STATUS_UNEXECUTED,
                            "test": TEST_DATA_ENDPOINT_ELASTIC
                        },
                        {
                            "status": STATUS_CONCLUSIVE,
                            "test": TEST_DATA_ENDPOINT_HTTP
                        }
                    ]
                }
            ],
            DEVICES: [
                {
                    "directive": "endpoint_security",
                    "status": "Conclusive",
                    "tests": [
                        {
                            "status": "Conclusive",
                            "test": "endpoint_security_exists"
                        },
                        {
                            "status": "Unexecuted",
                            "test": "machine_exploited"
                        }
                    ]
                }
            ],
            NETWORKS: [
                {
                    "directive": "segmentation",
                    "status": "Unexecuted",
                    "tests": [
                        {
                            "status": "Unexecuted",
                            "test": "segmentation"
                        }
                    ]
                },
                {
                    "directive": "user_behaviour",
                    "status": STATUS_INCONCLUSIVE,
                    "tests": [
                        {
                            "status": STATUS_INCONCLUSIVE,
                            "test": TEST_SCHEDULED_EXECUTION
                        }
                    ]
                },
                {
                    "directive": "analyze_network_traffic",
                    "status": "Unexecuted",
                    "tests": [
                        {
                            "status": "Unexecuted",
                            "test": "malicious_activity_timeline"
                        }
                    ]
                }
            ],
            PEOPLE: [
                {
                    "directive": "user_behaviour",
                    "status": STATUS_INCONCLUSIVE,
                    "tests": [
                        {
                            "status": STATUS_INCONCLUSIVE,
                            "test": TEST_SCHEDULED_EXECUTION
                        }
                    ]
                }
            ],
            "Visibility & Analytics": [
                {
                    "directive": DIRECTIVE_ANALYZE_NETWORK_TRAFFIC,
                    "status": STATUS_UNEXECUTED,
                    "tests": [
                        {
                            "status": STATUS_UNEXECUTED,
                            "test": TEST_ACTIVITY_TIMELINE
                        }
                    ]
                }
            ],
            "Workloads": []
        }

        self.assertEquals(ZeroTrustService.get_directives_status(), expected)
