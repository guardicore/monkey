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
TEST_STATUSES = (STATUS_CONCLUSIVE, STATUS_INCONCLUSIVE, STATUS_POSITIVE, STATUS_UNEXECUTED)

TEST_DATA_ENDPOINT_ELASTIC = u"unencrypted_data_endpoint_elastic"
TEST_DATA_ENDPOINT_HTTP = u"unencrypted_data_endpoint_http"
TEST_MACHINE_EXPLOITED = u"machine_exploited"
TEST_ENDPOINT_SECURITY_EXISTS = u"endpoint_security_exists"
TEST_SCHEDULED_EXECUTION = u"scheduled_execution"
TEST_ACTIVITY_TIMELINE = u"malicious_activity_timeline"
TEST_SEGMENTATION = u"segmentation"
TESTS = (
    TEST_SEGMENTATION,
    TEST_ACTIVITY_TIMELINE,
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
FINDING_FORMAT_KEY = u"finding_format"
EXPLANATION_KEY = u"explanation"
TESTS_MAP = {
    TEST_SEGMENTATION: {
        EXPLANATION_KEY: u"The Monkey tried to scan and find machines that it can communicate with from the machine it's running on, that belong to different network segments.",
        FINDING_FORMAT_KEY: u"The Monkey from {ORIGIN} communicated with a machine on a different segment.",
        DIRECTIVE_KEY: DIRECTIVE_SEGMENTATION,
        PILLARS_KEY: [NETWORKS],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_POSITIVE, STATUS_CONCLUSIVE]
    },
    TEST_ACTIVITY_TIMELINE: {
        EXPLANATION_KEY: u"The Monkeys in the network performed malicious-looking actions, like scanning and attempting exploitation.",
        FINDING_FORMAT_KEY: u"Malicious activity performed by the Monkeys. See 'events' for detailed information.",
        DIRECTIVE_KEY: DIRECTIVE_ANALYZE_NETWORK_TRAFFIC,
        PILLARS_KEY: [NETWORKS],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_INCONCLUSIVE]
    },
    TEST_ENDPOINT_SECURITY_EXISTS: {
        EXPLANATION_KEY: u"The Monkey checked if there is an active process of an endpoint security software.",
        FINDING_FORMAT_KEY: u"The Monkey on {ORIGIN} found no active endpoint security processes.",
        DIRECTIVE_KEY: DIRECTIVE_ENDPOINT_SECURITY,
        PILLARS_KEY: [DEVICES],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_CONCLUSIVE, STATUS_POSITIVE]
    },
    TEST_MACHINE_EXPLOITED: {
        EXPLANATION_KEY: u"The Monkey tries to exploit machines in order to breach them and propagate in the network.",
        FINDING_FORMAT_KEY: u"The Monkey on {ORIGIN} attempted to exploit a machine on {TARGET}.",
        DIRECTIVE_KEY: DIRECTIVE_ENDPOINT_SECURITY,
        PILLARS_KEY: [DEVICES],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_CONCLUSIVE, STATUS_INCONCLUSIVE]
    },
    TEST_SCHEDULED_EXECUTION: {
        EXPLANATION_KEY: "The Monkey was executed in a scheduled manner.",
        FINDING_FORMAT_KEY: "The Monkey on {ORIGIN} started running in an executed manner.",
        DIRECTIVE_KEY: DIRECTIVE_USER_BEHAVIOUR,
        PILLARS_KEY: [PEOPLE, NETWORKS],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_INCONCLUSIVE]
    },
    TEST_DATA_ENDPOINT_ELASTIC: {
        EXPLANATION_KEY: u"The Monkey scanned for unencrypted access to ElasticSearch instances.",
        FINDING_FORMAT_KEY: u"The Monkey on {ORIGIN} found an open ElasticSearch instance.",
        DIRECTIVE_KEY: DIRECTIVE_DATA_TRANSIT,
        PILLARS_KEY: [DATA],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_CONCLUSIVE, STATUS_POSITIVE]
    },
    TEST_DATA_ENDPOINT_HTTP: {
        EXPLANATION_KEY: u"The Monkey scanned for unencrypted access to HTTP servers.",
        FINDING_FORMAT_KEY: u"The Monkey on {ORIGIN} found an open HTTP server.",
        DIRECTIVE_KEY: DIRECTIVE_DATA_TRANSIT,
        PILLARS_KEY: [DATA],
        POSSIBLE_STATUSES_KEY: [STATUS_UNEXECUTED, STATUS_CONCLUSIVE, STATUS_POSITIVE]
    },
}
EVENT_TYPE_ISLAND = "island"
EVENT_TYPE_MONKEY_NETWORK = "monkey_network"
EVENT_TYPE_MONKEY_LOCAL = "monkey_local"
EVENT_TYPES = (EVENT_TYPE_MONKEY_LOCAL, EVENT_TYPE_MONKEY_NETWORK, EVENT_TYPE_ISLAND)