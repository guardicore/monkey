"""
This file contains all the static data relating to Zero Trust. It is mostly used in the zero trust report generation and
in creating findings.

This file contains static mappings between zero trust components such as: pillars, recommendations, tests, statuses.
Some of the mappings are computed when this module is loaded.
"""

AUTOMATION_ORCHESTRATION = u"Automation & Orchestration"
VISIBILITY_ANALYTICS = u"Visibility & Analytics"
WORKLOADS = u"Workloads"
DEVICES = u"Devices"
NETWORKS = u"Networks"
PEOPLE = u"People"
DATA = u"Data"
PILLARS = (DATA, PEOPLE, NETWORKS, DEVICES, WORKLOADS, VISIBILITY_ANALYTICS, AUTOMATION_ORCHESTRATION)

STATUS_UNEXECUTED = u"Unexecuted"
STATUS_PASSED = u"Passed"
STATUS_INCONCLUSIVE = u"Inconclusive"
STATUS_FAILED = u"Failed"
# Don't change order! The statuses are ordered by importance/severity.
ORDERED_TEST_STATUSES = [STATUS_FAILED, STATUS_INCONCLUSIVE, STATUS_PASSED, STATUS_UNEXECUTED]

TEST_DATA_ENDPOINT_ELASTIC = u"unencrypted_data_endpoint_elastic"
TEST_DATA_ENDPOINT_HTTP = u"unencrypted_data_endpoint_http"
TEST_MACHINE_EXPLOITED = u"machine_exploited"
TEST_ENDPOINT_SECURITY_EXISTS = u"endpoint_security_exists"
TEST_SCHEDULED_EXECUTION = u"scheduled_execution"
TEST_MALICIOUS_ACTIVITY_TIMELINE = u"malicious_activity_timeline"
TEST_SEGMENTATION = u"segmentation"
TESTS = (
    TEST_SEGMENTATION,
    TEST_MALICIOUS_ACTIVITY_TIMELINE,
    TEST_SCHEDULED_EXECUTION,
    TEST_ENDPOINT_SECURITY_EXISTS,
    TEST_MACHINE_EXPLOITED,
    TEST_DATA_ENDPOINT_HTTP,
    TEST_DATA_ENDPOINT_ELASTIC
)

RECOMMENDATION_DATA_TRANSIT = u"data_transit"
RECOMMENDATION_ENDPOINT_SECURITY = u"endpoint_security"
RECOMMENDATION_USER_BEHAVIOUR = u"user_behaviour"
RECOMMENDATION_ANALYZE_NETWORK_TRAFFIC = u"analyze_network_traffic"
RECOMMENDATION_SEGMENTATION = u"segmentation"
RECOMMENDATIONS = {
    RECOMMENDATION_SEGMENTATION: u"Apply segmentation and micro-segmentation inside your network.",
    RECOMMENDATION_ANALYZE_NETWORK_TRAFFIC: u"Analyze network traffic for malicious activity.",
    RECOMMENDATION_USER_BEHAVIOUR: u"Adopt security user behavior analytics.",
    RECOMMENDATION_ENDPOINT_SECURITY: u"Use anti-virus and other traditional endpoint security solutions.",
    RECOMMENDATION_DATA_TRANSIT: u"Secure data at transit by encrypting it."
}

POSSIBLE_STATUSES_KEY = u"possible_statuses"
PILLARS_KEY = u"pillars"
RECOMMENDATION_KEY = u"recommendation_key"
FINDING_EXPLANATION_BY_STATUS_KEY = u"finding_explanation"
TEST_EXPLANATION_KEY = u"explanation"
TESTS_MAP = {
    TEST_SEGMENTATION: {
        TEST_EXPLANATION_KEY: u"The Monkey tried to scan and find machines that it can communicate with from the machine it's running on, that belong to different network segments.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_FAILED: "Monkey performed cross-segment communication. Check firewall rules and logs.",
            STATUS_PASSED: "Monkey couldn't perform cross-segment communication. If relevant, check firewall logs."
        },
        RECOMMENDATION_KEY: RECOMMENDATION_SEGMENTATION,
        PILLARS_KEY: [NETWORKS],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_PASSED, STATUS_FAILED]
    },
    TEST_MALICIOUS_ACTIVITY_TIMELINE: {
        TEST_EXPLANATION_KEY: u"The Monkeys in the network performed malicious-looking actions, like scanning and attempting exploitation.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_INCONCLUSIVE: "Monkey performed malicious actions in the network. Check SOC logs and alerts."
        },
        RECOMMENDATION_KEY: RECOMMENDATION_ANALYZE_NETWORK_TRAFFIC,
        PILLARS_KEY: [NETWORKS, VISIBILITY_ANALYTICS],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_INCONCLUSIVE]
    },
    TEST_ENDPOINT_SECURITY_EXISTS: {
        TEST_EXPLANATION_KEY: u"The Monkey checked if there is an active process of an endpoint security software.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_FAILED: "Monkey didn't find ANY active endpoint security processes. Install and activate anti-virus software on endpoints.",
            STATUS_PASSED: "Monkey found active endpoint security processes. Check their logs to see if Monkey was a security concern."
        },
        RECOMMENDATION_KEY: RECOMMENDATION_ENDPOINT_SECURITY,
        PILLARS_KEY: [DEVICES],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_FAILED, STATUS_PASSED]
    },
    TEST_MACHINE_EXPLOITED: {
        TEST_EXPLANATION_KEY: u"The Monkey tries to exploit machines in order to breach them and propagate in the network.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_FAILED: "Monkey successfully exploited endpoints. Check IDS/IPS logs to see activity recognized and see which endpoints were compromised.",
            STATUS_PASSED: "Monkey didn't manage to exploit an endpoint."
        },
        RECOMMENDATION_KEY: RECOMMENDATION_ENDPOINT_SECURITY,
        PILLARS_KEY: [DEVICES],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_FAILED, STATUS_INCONCLUSIVE]
    },
    TEST_SCHEDULED_EXECUTION: {
        TEST_EXPLANATION_KEY: "The Monkey was executed in a scheduled manner.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_INCONCLUSIVE: "Monkey was executed in a scheduled manner. Locate this activity in User-Behavior security software.",
            STATUS_PASSED: "Monkey failed to execute in a scheduled manner."
        },
        RECOMMENDATION_KEY: RECOMMENDATION_USER_BEHAVIOUR,
        PILLARS_KEY: [PEOPLE, NETWORKS],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_INCONCLUSIVE]
    },
    TEST_DATA_ENDPOINT_ELASTIC: {
        TEST_EXPLANATION_KEY: u"The Monkey scanned for unencrypted access to ElasticSearch instances.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_FAILED: "Monkey accessed ElasticSearch instances. Limit access to data by encrypting it in in-transit.",
            STATUS_PASSED: "Monkey didn't find open ElasticSearch instances. If you have such instances, look for alerts that indicate attempts to access them."
        },
        RECOMMENDATION_KEY: RECOMMENDATION_DATA_TRANSIT,
        PILLARS_KEY: [DATA],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_FAILED, STATUS_PASSED]
    },
    TEST_DATA_ENDPOINT_HTTP: {
        TEST_EXPLANATION_KEY: u"The Monkey scanned for unencrypted access to HTTP servers.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_FAILED: "Monkey accessed HTTP servers. Limit access to data by encrypting it in in-transit.",
            STATUS_PASSED: "Monkey didn't find open HTTP servers. If you have such servers, look for alerts that indicate attempts to access them."
        },
        RECOMMENDATION_KEY: RECOMMENDATION_DATA_TRANSIT,
        PILLARS_KEY: [DATA],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_FAILED, STATUS_PASSED]
    },
}

EVENT_TYPE_ISLAND = "island"
EVENT_TYPE_MONKEY_NETWORK = "monkey_network"
EVENT_TYPE_MONKEY_LOCAL = "monkey_local"
EVENT_TYPES = (EVENT_TYPE_MONKEY_LOCAL, EVENT_TYPE_MONKEY_NETWORK, EVENT_TYPE_ISLAND)

PILLARS_TO_TESTS = {
    DATA: [],
    PEOPLE: [],
    NETWORKS: [],
    DEVICES: [],
    WORKLOADS: [],
    VISIBILITY_ANALYTICS: [],
    AUTOMATION_ORCHESTRATION: []
}

RECOMMENDATIONS_TO_TESTS = {}

RECOMMENDATIONS_TO_PILLARS = {}


def populate_mappings():
    populate_pillars_to_tests()
    populate_recommendations_to_tests()
    populate_recommendations_to_pillars()


def populate_pillars_to_tests():
    for pillar in PILLARS:
        for test, test_info in TESTS_MAP.items():
            if pillar in test_info[PILLARS_KEY]:
                PILLARS_TO_TESTS[pillar].append(test)


def populate_recommendations_to_tests():
    for single_recommendation in RECOMMENDATIONS:
        RECOMMENDATIONS_TO_TESTS[single_recommendation] = []
    for test, test_info in TESTS_MAP.items():
        RECOMMENDATIONS_TO_TESTS[test_info[RECOMMENDATION_KEY]].append(test)


def populate_recommendations_to_pillars():
    for recommendation, recommendation_tests in RECOMMENDATIONS_TO_TESTS.items():
        recommendations_pillars = set()
        for test in recommendation_tests:
            for pillar in TESTS_MAP[test][PILLARS_KEY]:
                recommendations_pillars.add(pillar)
        RECOMMENDATIONS_TO_PILLARS[recommendation] = recommendations_pillars
