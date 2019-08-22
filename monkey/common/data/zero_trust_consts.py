"""
This file contains all the static data relating to Zero Trust. It is mostly used in the zero trust report generation and
in creating findings.

This file contains static mappings between zero trust components such as: pillars, directives, tests, statuses. Some of
the mappings are computed when this module is loaded.
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
STATUS_POSITIVE = u"Positive"
STATUS_INCONCLUSIVE = u"Inconclusive"
STATUS_CONCLUSIVE = u"Conclusive"
# Don't change order! The statuses are ordered by importance/severity.
ORDERED_TEST_STATUSES = [STATUS_CONCLUSIVE, STATUS_INCONCLUSIVE, STATUS_POSITIVE, STATUS_UNEXECUTED]

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

DIRECTIVE_DATA_TRANSIT = u"data_transit"
DIRECTIVE_ENDPOINT_SECURITY = u"endpoint_security"
DIRECTIVE_USER_BEHAVIOUR = u"user_behaviour"
DIRECTIVE_ANALYZE_NETWORK_TRAFFIC = u"analyze_network_traffic"
DIRECTIVE_SEGMENTATION = u"segmentation"
DIRECTIVES = {
    DIRECTIVE_SEGMENTATION: u"Apply segmentation and micro-segmentation inside your network.",
    DIRECTIVE_ANALYZE_NETWORK_TRAFFIC: u"Analyze network traffic for malicious activity.",
    DIRECTIVE_USER_BEHAVIOUR: u"Adopt security user behavior analytics.",
    DIRECTIVE_ENDPOINT_SECURITY: u"Use anti-virus and other traditional endpoint security solutions.",
    DIRECTIVE_DATA_TRANSIT: u"Secure data at transit by encrypting it."
}

POSSIBLE_STATUSES_KEY = u"possible_statuses"
PILLARS_KEY = u"pillars"
DIRECTIVE_KEY = u"directive_key"
FINDING_EXPLANATION_BY_STATUS_KEY = u"finding_explanation"
TEST_EXPLANATION_KEY = u"explanation"
TESTS_MAP = {
    TEST_SEGMENTATION: {
        TEST_EXPLANATION_KEY: u"The Monkey tried to scan and find machines that it can communicate with from the machine it's running on, that belong to different network segments.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_CONCLUSIVE: "Monkey performed cross-segment communication. Check firewall rules and logs.",
            STATUS_POSITIVE: "Monkey couldn't perform cross-segment communication. If relevant, check firewall logs."
        },
        DIRECTIVE_KEY: DIRECTIVE_SEGMENTATION,
        PILLARS_KEY: [NETWORKS],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_POSITIVE, STATUS_CONCLUSIVE]
    },
    TEST_MALICIOUS_ACTIVITY_TIMELINE: {
        TEST_EXPLANATION_KEY: u"The Monkeys in the network performed malicious-looking actions, like scanning and attempting exploitation.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_INCONCLUSIVE: "Monkey performed malicious actions in the network. Check SOC logs and alerts."
        },
        DIRECTIVE_KEY: DIRECTIVE_ANALYZE_NETWORK_TRAFFIC,
        PILLARS_KEY: [NETWORKS, VISIBILITY_ANALYTICS],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_INCONCLUSIVE]
    },
    TEST_ENDPOINT_SECURITY_EXISTS: {
        TEST_EXPLANATION_KEY: u"The Monkey checked if there is an active process of an endpoint security software.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_CONCLUSIVE: "Monkey didn't find ANY active endpoint security processes. Install and activate anti-virus software on endpoints.",
            STATUS_POSITIVE: "Monkey found active endpoint security processes. Check their logs to see if Monkey was a security concern."
        },
        DIRECTIVE_KEY: DIRECTIVE_ENDPOINT_SECURITY,
        PILLARS_KEY: [DEVICES],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_CONCLUSIVE, STATUS_POSITIVE]
    },
    TEST_MACHINE_EXPLOITED: {
        TEST_EXPLANATION_KEY: u"The Monkey tries to exploit machines in order to breach them and propagate in the network.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_CONCLUSIVE: "Monkey successfully exploited endpoints. Check IDS/IPS logs to see activity recognized and see which endpoints were compromised.",
            STATUS_INCONCLUSIVE: "Monkey tried exploiting endpoints. Check IDS/IPS logs to see activity recognized."
        },
        DIRECTIVE_KEY: DIRECTIVE_ENDPOINT_SECURITY,
        PILLARS_KEY: [DEVICES],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_CONCLUSIVE, STATUS_INCONCLUSIVE]
    },
    TEST_SCHEDULED_EXECUTION: {
        TEST_EXPLANATION_KEY: "The Monkey was executed in a scheduled manner.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_INCONCLUSIVE: "Monkey was executed in a scheduled manner. Locate this activity in User-Behavior security software."
        },
        DIRECTIVE_KEY: DIRECTIVE_USER_BEHAVIOUR,
        PILLARS_KEY: [PEOPLE, NETWORKS],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_INCONCLUSIVE]
    },
    TEST_DATA_ENDPOINT_ELASTIC: {
        TEST_EXPLANATION_KEY: u"The Monkey scanned for unencrypted access to ElasticSearch instances.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_CONCLUSIVE: "Monkey accessed ElasticSearch instances. Limit access to data by encrypting it in in-transit.",
            STATUS_POSITIVE: "Monkey didn't find open ElasticSearch instances. If you have such instances, look for alerts that indicate attempts to access them."
        },
        DIRECTIVE_KEY: DIRECTIVE_DATA_TRANSIT,
        PILLARS_KEY: [DATA],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_CONCLUSIVE, STATUS_POSITIVE]
    },
    TEST_DATA_ENDPOINT_HTTP: {
        TEST_EXPLANATION_KEY: u"The Monkey scanned for unencrypted access to HTTP servers.",
        FINDING_EXPLANATION_BY_STATUS_KEY: {
            STATUS_CONCLUSIVE: "Monkey accessed HTTP servers. Limit access to data by encrypting it in in-transit.",
            STATUS_POSITIVE: "Monkey didn't find open HTTP servers. If you have such servers, look for alerts that indicate attempts to access them."
        },
        DIRECTIVE_KEY: DIRECTIVE_DATA_TRANSIT,
        PILLARS_KEY: [DATA],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_CONCLUSIVE, STATUS_POSITIVE]
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

DIRECTIVES_TO_TESTS = {}

DIRECTIVES_TO_PILLARS = {}


def populate_mappings():
    populate_pillars_to_tests()
    populate_directives_to_tests()
    populate_directives_to_pillars()


def populate_pillars_to_tests():
    for pillar in PILLARS:
        for test, test_info in TESTS_MAP.items():
            if pillar in test_info[PILLARS_KEY]:
                PILLARS_TO_TESTS[pillar].append(test)


def populate_directives_to_tests():
    for single_directive in DIRECTIVES:
        DIRECTIVES_TO_TESTS[single_directive] = []
    for test, test_info in TESTS_MAP.items():
        DIRECTIVES_TO_TESTS[test_info[DIRECTIVE_KEY]].append(test)


def populate_directives_to_pillars():
    for directive, directive_tests in DIRECTIVES_TO_TESTS.items():
        directive_pillars = set()
        for test in directive_tests:
            for pillar in TESTS_MAP[test][PILLARS_KEY]:
                directive_pillars.add(pillar)
        DIRECTIVES_TO_PILLARS[directive] = directive_pillars
