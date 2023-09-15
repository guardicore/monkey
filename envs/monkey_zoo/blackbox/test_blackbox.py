import logging
import os
import random
from copy import deepcopy
from http import HTTPStatus
from threading import Thread
from time import sleep
from typing import Iterable, List, Optional, Sequence
from uuid import uuid4

import pytest
import requests
from treelib import Tree

from common import OperatingSystem
from common.types import OTP, SocketAddress
from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import CommunicationAnalyzer
from envs.monkey_zoo.blackbox.analyzers.stolen_credentials_analyzer import StolenCredentialsAnalyzer
from envs.monkey_zoo.blackbox.analyzers.zerologon_analyzer import ZerologonAnalyzer
from envs.monkey_zoo.blackbox.expected_credentials import (
    expected_credentials_depth_1_a,
    expected_credentials_depth_2_a,
)
from envs.monkey_zoo.blackbox.island_client.agent_requests import AgentRequests
from envs.monkey_zoo.blackbox.island_client.i_monkey_island_requests import IMonkeyIslandRequests
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import (
    GET_AGENT_EVENTS_ENDPOINT,
    GET_AGENT_OTP_ENDPOINT,
    GET_AGENTS_ENDPOINT,
    GET_MACHINES_ENDPOINT,
    ISLAND_LOG_ENDPOINT,
    LOGOUT_ENDPOINT,
    MonkeyIslandClient,
)
from envs.monkey_zoo.blackbox.island_client.monkey_island_requests import MonkeyIslandRequests
from envs.monkey_zoo.blackbox.island_client.reauthorizing_monkey_island_requests import (
    ReauthorizingMonkeyIslandRequests,
)
from envs.monkey_zoo.blackbox.island_client.test_configuration_parser import get_target_ips
from envs.monkey_zoo.blackbox.log_handlers.test_logs_handler import TestLogsHandler
from envs.monkey_zoo.blackbox.test_configurations import (
    credentials_reuse_ssh_key_test_configuration,
    depth_1_a_test_configuration,
    depth_2_a_test_configuration,
    depth_3_a_test_configuration,
    depth_4_a_test_configuration,
    smb_pth_test_configuration,
    zerologon_test_configuration,
)
from envs.monkey_zoo.blackbox.test_configurations.test_configuration import TestConfiguration
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest
from envs.monkey_zoo.blackbox.utils.gcp_machine_handlers import (
    initialize_gcp_client,
    start_machines,
    stop_machines,
)
from monkey_island.cc.models import Agent
from monkey_island.cc.services.authentication_service.flask_resources.agent_otp import (
    MAX_OTP_REQUESTS_PER_SECOND,
)

DEFAULT_TIMEOUT_SECONDS = 2 * 60 + 30
MACHINE_BOOTUP_WAIT_SECONDS = 30
LOG_DIR_PATH = "./logs"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="session")
def GCPHandler(request, no_gcp, gcp_machines_to_start):
    if no_gcp:
        return
    if len(gcp_machines_to_start) == 0:
        logger.info("No GCP machines to start.")
    else:
        logger.info(f"MACHINES TO START: {gcp_machines_to_start}")

        try:
            initialize_gcp_client()
            start_machines(gcp_machines_to_start)
        except Exception as e:
            logger.error("GCP Handler failed to initialize: %s." % e)
            pytest.exit("Encountered an error while starting GCP machines. Stopping the tests.")
        wait_machine_bootup()

        def fin():
            stop_machines(gcp_machines_to_start)

        request.addfinalizer(fin)


@pytest.fixture(autouse=True, scope="session")
def delete_logs():
    logger.info("Deleting monkey logs before new tests.")
    TestLogsHandler.delete_log_folder_contents(TestMonkeyBlackbox.get_log_dir_path())


def wait_machine_bootup():
    sleep(MACHINE_BOOTUP_WAIT_SECONDS)


@pytest.fixture(scope="session")
def monkey_island_requests(island) -> IMonkeyIslandRequests:
    return MonkeyIslandRequests(island)


@pytest.fixture(scope="session")
def island_client(monkey_island_requests):
    client_established = False
    try:
        reauthorizing_island_requests = ReauthorizingMonkeyIslandRequests(monkey_island_requests)
        island_client_object = MonkeyIslandClient(reauthorizing_island_requests)
        client_established = island_client_object.get_api_status()
    except Exception:
        logging.exception("Got an exception while trying to establish connection to the Island.")
    finally:
        if not client_established:
            pytest.exit("BB tests couldn't establish communication to the island.")

    yield island_client_object


@pytest.fixture(autouse=True, scope="session")
def setup_island(island_client):
    logging.info("Registering a new user")
    island_client.register()

    logging.info("Installing all available plugins")
    island_client.install_agent_plugins()


@pytest.mark.parametrize(
    "authenticated_endpoint",
    [
        GET_AGENTS_ENDPOINT,
        ISLAND_LOG_ENDPOINT,
        GET_MACHINES_ENDPOINT,
    ],
)
def test_island_logout(island, authenticated_endpoint):
    monkey_island_requests = MonkeyIslandRequests(island)
    # Prove that we can't access authenticated endpoints without logging in
    resp = monkey_island_requests.get(authenticated_endpoint)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED

    # Prove that we can access authenticated endpoints after logging in
    monkey_island_requests.login()
    resp = monkey_island_requests.get(authenticated_endpoint)
    assert resp.ok

    # Log out - NOTE: This is an "out-of-band" call to logout. DO NOT call
    # `monkey_island_request.logout()`. This could allow implementation details of the
    # MonkeyIslandRequests class to cause false positives.
    monkey_island_requests.post(LOGOUT_ENDPOINT, data=None)

    # Prove that we can't access authenticated endpoints after logging out
    resp = monkey_island_requests.get(authenticated_endpoint)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


def test_logout_invalidates_all_tokens(island):
    monkey_island_requests_1 = MonkeyIslandRequests(island)
    monkey_island_requests_2 = MonkeyIslandRequests(island)

    monkey_island_requests_1.login()
    monkey_island_requests_2.login()

    # Prove that we can access authenticated endpoints after logging in
    resp_1 = monkey_island_requests_1.get(GET_AGENTS_ENDPOINT)
    resp_2 = monkey_island_requests_2.get(GET_AGENTS_ENDPOINT)
    assert resp_1.ok
    assert resp_2.ok

    # Log out - NOTE: This is an "out-of-band" call to logout. DO NOT call
    # `monkey_island_request.logout()`. This could allow implementation details of the
    # MonkeyIslandRequests class to cause false positives.
    # NOTE: Logout is ONLY called on monkey_island_requests_1. This is to prove that
    # monkey_island_requests_2 also gets logged out.
    monkey_island_requests_1.post(LOGOUT_ENDPOINT, data=None)

    # Prove monkey_island_requests_2 can't authenticate after monkey_island_requests_1 logs out.
    resp = monkey_island_requests_2.get(GET_AGENTS_ENDPOINT)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


AGENT_OTP_LOGIN_ENDPOINT = "/api/agent-otp-login"


@pytest.mark.parametrize(
    "request_callback, successful_request_status, max_requests_per_second",
    [
        (lambda mir: mir.get(GET_AGENT_OTP_ENDPOINT), HTTPStatus.OK, MAX_OTP_REQUESTS_PER_SECOND),
    ],
)
def test_rate_limit(
    monkey_island_requests, request_callback, successful_request_status, max_requests_per_second
):
    monkey_island_requests.login()
    threads = []
    response_codes = []

    def make_request(monkey_island_requests, request_callback):
        response = request_callback(monkey_island_requests)
        response_codes.append(response.status_code)

    for _ in range(0, max_requests_per_second + 1):
        t = Thread(
            target=make_request, args=(monkey_island_requests, request_callback), daemon=True
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    assert response_codes.count(successful_request_status) == max_requests_per_second
    assert response_codes.count(HTTPStatus.TOO_MANY_REQUESTS) == 1


RATE_LIMIT_AGENT1_ID = uuid4()
RATE_LIMIT_AGENT2_ID = uuid4()


@pytest.mark.skip(
    reason="This test will fail if the requests cannot be made in less than 1 second."
)
@pytest.mark.parametrize(
    "request_callback, successful_request_status, max_requests_per_second",
    [
        (lambda mir: mir.get(GET_AGENT_OTP_ENDPOINT), HTTPStatus.OK, MAX_OTP_REQUESTS_PER_SECOND),
    ],
)
def test_rate_limit__agent_user(
    island,
    monkey_island_requests,
    request_callback,
    successful_request_status,
    max_requests_per_second,
):
    monkey_island_requests.login()
    response = monkey_island_requests.get(GET_AGENT_OTP_ENDPOINT)
    otp1 = response.json()["otp"]
    response = monkey_island_requests.get(GET_AGENT_OTP_ENDPOINT)
    otp2 = response.json()["otp"]

    agent1_requests = AgentRequests(island, RATE_LIMIT_AGENT1_ID, OTP(otp1))
    agent1_requests.login()
    agent2_requests = AgentRequests(island, RATE_LIMIT_AGENT2_ID, OTP(otp2))
    agent2_requests.login()

    threads = []
    response_codes1: List[int] = []
    response_codes2: List[int] = []

    def make_request(agent_requests, request_callback, response_codes):
        response = request_callback(agent_requests)
        response_codes.append(response.status_code)

    for _ in range(0, max_requests_per_second + 1):
        t1 = Thread(
            target=make_request,
            args=(agent1_requests, request_callback, response_codes1),
            daemon=True,
        )
        t1.start()
        t2 = Thread(
            target=make_request,
            args=(agent2_requests, request_callback, response_codes2),
            daemon=True,
        )
        t2.start()
        threads.append(t1)
        threads.append(t2)

    for t in threads:
        t.join()

    assert response_codes1.count(successful_request_status) == max_requests_per_second
    assert response_codes1.count(HTTPStatus.TOO_MANY_REQUESTS) == 1
    assert response_codes2.count(successful_request_status) == max_requests_per_second
    assert response_codes2.count(HTTPStatus.TOO_MANY_REQUESTS) == 1


def test_refresh_access_token(monkey_island_requests):
    monkey_island_requests.login()
    original_token = monkey_island_requests.token

    monkey_island_requests.refresh_access_token()
    refreshed_token = monkey_island_requests.token

    assert original_token != refreshed_token

    with pytest.raises(requests.exceptions.HTTPError):
        monkey_island_requests_copy = deepcopy(monkey_island_requests)
        monkey_island_requests_copy.token = original_token
        monkey_island_requests_copy.refresh_access_token()

    monkey_island_requests.refresh_access_token()
    assert refreshed_token != monkey_island_requests.token


UUID = uuid4()
AGENT_EVENTS_ENDPOINT = "/api/agent-events"
AGENT_HEARTBEAT_ENDPOINT = f"/api/agent/{UUID}/heartbeat"
PUT_LOG_ENDPOINT = f"/api/agent-logs/{UUID}"
GET_AGENT_PLUGINS_ENDPOINT = "/api/agent-plugins/host/type/name"
GET_AGENT_SIGNALS_ENDPOINT = f"/api/agent-signals/{UUID}"


def test_island__cannot_access_nonisland_endpoints(island):
    island_requests = MonkeyIslandRequests(island)
    island_requests.login()

    assert (
        island_requests.post(AGENT_EVENTS_ENDPOINT, data=None).status_code == HTTPStatus.FORBIDDEN
    )
    assert (
        island_requests.post(AGENT_HEARTBEAT_ENDPOINT, data=None).status_code
        == HTTPStatus.FORBIDDEN
    )
    assert island_requests.put(PUT_LOG_ENDPOINT, data=None).status_code == HTTPStatus.FORBIDDEN
    assert island_requests.get(GET_AGENT_PLUGINS_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert (
        island_requests.get("/api/agent-plugins/plugin-type/plugin-name/manifest").status_code
        == HTTPStatus.FORBIDDEN
    )
    assert island_requests.get(GET_AGENT_SIGNALS_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert island_requests.post(GET_AGENTS_ENDPOINT, data=None).status_code == HTTPStatus.FORBIDDEN


REQUESTS_AGENT_ID = UUID
TERMINATE_AGENTS_ENDPOINT = "/api/agent-signals/terminate-all-agents"
CLEAR_SIMULATION_DATA_ENDPOINT = "/api/clear-simulation-data"
MONKEY_EXPLOITATION_ENDPOINT = "/api/exploitations/monkey"
GET_ISLAND_LOG_ENDPOINT = "/api/island/log"
ISLAND_RUN_ENDPOINT = "/api/local-monkey"
GET_NODES_ENDPOINT = "/api/nodes"
PROPAGATION_CREDENTIALS_ENDPOINT = "/api/propagation-credentials"
GET_RANSOMWARE_REPORT_ENDPOINT = "/api/report/ransomware"
REMOTE_RUN_ENDPOINT = "/api/remote-monkey"
GET_REPORT_STATUS_ENDPOINT = "/api/report-generation-status"
RESET_AGENT_CONFIG_ENDPOINT = "/api/reset-agent-configuration"
GET_SECURITY_REPORT_ENDPOINT = "/api/report/security"
GET_ISLAND_VERSION_ENDPOINT = "/api/island/version"
PUT_AGENT_CONFIG_ENDPOINT = "/api/agent-configuration"
INSTALL_AGENT_PLUGIN_ENDPOINT = "/api/install-agent-plugin"
AVAILABLE_AGENT_PLUGIN_INDEX_ENDPOINT = "/api/agent-plugins/available/index?force_refresh=true"
UNINSTALL_AGENT_PLUGIN_ENDPOINT = "/api/uninstall-agent-plugin"


def test_agent__cannot_access_nonagent_endpoints(island):
    island_requests = MonkeyIslandRequests(island)
    island_requests.login()
    response = island_requests.get(GET_AGENT_OTP_ENDPOINT)
    otp = response.json()["otp"]

    agent_requests = AgentRequests(island, REQUESTS_AGENT_ID, OTP(otp))
    agent_requests.login()

    assert agent_requests.get(GET_AGENT_EVENTS_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert agent_requests.get(PUT_LOG_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert (
        agent_requests.post(TERMINATE_AGENTS_ENDPOINT, data=None).status_code
        == HTTPStatus.FORBIDDEN
    )
    assert agent_requests.get(GET_AGENTS_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert (
        agent_requests.post(CLEAR_SIMULATION_DATA_ENDPOINT, data=None).status_code
        == HTTPStatus.FORBIDDEN
    )
    assert agent_requests.get(MONKEY_EXPLOITATION_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert agent_requests.get(GET_ISLAND_LOG_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert agent_requests.post(ISLAND_RUN_ENDPOINT, data=None).status_code == HTTPStatus.FORBIDDEN
    assert agent_requests.get(GET_MACHINES_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert agent_requests.get(GET_NODES_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert (
        agent_requests.put(PROPAGATION_CREDENTIALS_ENDPOINT, data=None).status_code
        == HTTPStatus.FORBIDDEN
    )
    assert agent_requests.get(GET_RANSOMWARE_REPORT_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert agent_requests.get(REMOTE_RUN_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert agent_requests.post(REMOTE_RUN_ENDPOINT, data=None).status_code == HTTPStatus.FORBIDDEN
    assert agent_requests.get(GET_REPORT_STATUS_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert (
        agent_requests.post(RESET_AGENT_CONFIG_ENDPOINT, data=None).status_code
        == HTTPStatus.FORBIDDEN
    )
    assert agent_requests.get(GET_SECURITY_REPORT_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert agent_requests.get(GET_ISLAND_VERSION_ENDPOINT).status_code == HTTPStatus.FORBIDDEN
    assert (
        agent_requests.put(PUT_AGENT_CONFIG_ENDPOINT, data=None).status_code == HTTPStatus.FORBIDDEN
    )
    assert (
        agent_requests.put(INSTALL_AGENT_PLUGIN_ENDPOINT, data=None).status_code
        == HTTPStatus.FORBIDDEN
    )
    assert (
        agent_requests.get(AVAILABLE_AGENT_PLUGIN_INDEX_ENDPOINT).status_code
        == HTTPStatus.FORBIDDEN
    )
    assert (
        agent_requests.post(UNINSTALL_AGENT_PLUGIN_ENDPOINT, data=None).status_code
        == HTTPStatus.FORBIDDEN
    )


def test_unauthenticated_user_cannot_access_API(island):
    island_requests = MonkeyIslandRequests(island)

    assert (
        island_requests.post(AGENT_EVENTS_ENDPOINT, data=None).status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert (
        island_requests.post(AGENT_HEARTBEAT_ENDPOINT, data=None).status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert island_requests.put(PUT_LOG_ENDPOINT, data=None).status_code == HTTPStatus.UNAUTHORIZED
    assert island_requests.get(GET_AGENT_PLUGINS_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert (
        island_requests.get("/api/agent-plugins/plugin-type/plugin-name/manifest").status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert island_requests.get(GET_AGENT_SIGNALS_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert (
        island_requests.post(GET_AGENTS_ENDPOINT, data=None).status_code == HTTPStatus.UNAUTHORIZED
    )
    assert island_requests.get(GET_AGENT_EVENTS_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert island_requests.get(PUT_LOG_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert (
        island_requests.post(TERMINATE_AGENTS_ENDPOINT, data=None).status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert island_requests.get(GET_AGENTS_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert (
        island_requests.post(CLEAR_SIMULATION_DATA_ENDPOINT, data=None).status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert island_requests.get(MONKEY_EXPLOITATION_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert island_requests.get(GET_ISLAND_LOG_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert (
        island_requests.post(ISLAND_RUN_ENDPOINT, data=None).status_code == HTTPStatus.UNAUTHORIZED
    )
    assert island_requests.get(GET_MACHINES_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert island_requests.get(GET_NODES_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert (
        island_requests.put(PROPAGATION_CREDENTIALS_ENDPOINT, data=None).status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert (
        island_requests.get(PROPAGATION_CREDENTIALS_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    )
    assert (
        island_requests.get(GET_RANSOMWARE_REPORT_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    )
    assert island_requests.get(REMOTE_RUN_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert (
        island_requests.post(REMOTE_RUN_ENDPOINT, data=None).status_code == HTTPStatus.UNAUTHORIZED
    )
    assert island_requests.get(GET_REPORT_STATUS_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert (
        island_requests.post(RESET_AGENT_CONFIG_ENDPOINT, data=None).status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert island_requests.get(GET_SECURITY_REPORT_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert island_requests.get(GET_ISLAND_VERSION_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED
    assert (
        island_requests.put(PUT_AGENT_CONFIG_ENDPOINT, data=None).status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert (
        island_requests.put(INSTALL_AGENT_PLUGIN_ENDPOINT, data=None).status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert (
        island_requests.get(AVAILABLE_AGENT_PLUGIN_INDEX_ENDPOINT).status_code
        == HTTPStatus.UNAUTHORIZED
    )
    assert (
        island_requests.post(UNINSTALL_AGENT_PLUGIN_ENDPOINT, data=None).status_code
        == HTTPStatus.UNAUTHORIZED
    )


LOGOUT_AGENT_ID = uuid4()


def test_agent_logout(island):
    island_requests = MonkeyIslandRequests(island)
    island_requests.login()
    response = island_requests.get(GET_AGENT_OTP_ENDPOINT)
    otp = response.json()["otp"]

    agent_requests = AgentRequests(island, LOGOUT_AGENT_ID, OTP(otp))
    agent_requests.login()

    agent_registration_dict = {
        "id": LOGOUT_AGENT_ID,
        "machine_hardware_id": 2,
        "start_time": "2022-08-18T18:46:48+00:00",
        "cc_server": SocketAddress.from_string(island).dict(simplify=True),
        "network_interfaces": [],
    }

    agent_requests.post(GET_AGENTS_ENDPOINT, data=agent_registration_dict)
    assert agent_requests.post(LOGOUT_ENDPOINT, data=None).status_code == HTTPStatus.OK

    # After logout, agent should not be able to access any endpoints
    assert agent_requests.get(GET_AGENT_OTP_ENDPOINT).status_code == HTTPStatus.UNAUTHORIZED


RANDBYTES_SIZE = 1024 * 1024 * 2  # 2MB
LINUX_DATA = [
    b"This is a string for Linux!",
    random.randbytes(RANDBYTES_SIZE),  # noqa: DUO102
    b"More strings",
    b"A much longer supercalifragilisticexpialidocious string to be included in the masque.",
]
WINDOWS_DATA = [
    b"This is a string for Windows!",
    random.randbytes(RANDBYTES_SIZE),  # noqa: DUO102
    LINUX_DATA[2],
    LINUX_DATA[3],
]


@pytest.mark.parametrize(
    "data, operating_system",
    [(LINUX_DATA, OperatingSystem.LINUX), (WINDOWS_DATA, OperatingSystem.WINDOWS)],
    ids=["Linux", "Windows"],
)
def test_masquerade(
    island_client: MonkeyIslandClient, data: Iterable[bytes], operating_system: OperatingSystem
):
    masque_data = b"\0".join(data)

    island_client.set_masque(masque_data)
    agent_binary = island_client.get_agent_binary(operating_system)

    for d in data:
        assert d in agent_binary


# NOTE: These test methods are ordered to give time for the slower zoo machines
# to boot up and finish starting services.
# noinspection PyUnresolvedReferences
class TestMonkeyBlackbox:
    @staticmethod
    def assert_unique_agent_hashes(agents: Sequence[Agent]):
        agent_hashes = [a.sha256 for a in agents]

        assert len(agent_hashes) == len(set(agent_hashes))

    @staticmethod
    def assert_depth_restriction(agents: Sequence[Agent], configured_depth: int):
        # Trying to add a node to the tree whose parent doesn't exist in the tree yet
        # raises `NodeIDAbsentError`. Sorting the agents by registration time prevents that.
        sorted_agents = sorted(agents, key=lambda agent: agent.registration_time)

        propagation_tree = Tree()
        for agent in sorted_agents:
            propagation_tree.create_node(tag=agent.id, identifier=agent.id, parent=agent.parent_id)

        assert propagation_tree.depth() <= configured_depth

    @staticmethod
    def run_exploitation_test(
        island_client: MonkeyIslandClient,
        test_configuration: TestConfiguration,
        test_name: str,
        timeout_in_seconds=DEFAULT_TIMEOUT_SECONDS,
        masque: Optional[bytes] = None,
    ):
        analyzer = CommunicationAnalyzer(
            island_client,
            get_target_ips(test_configuration),
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        exploitation_test = ExploitationTest(
            name=test_name,
            island_client=island_client,
            test_configuration=test_configuration,
            masque=masque,
            analyzers=[analyzer],
            timeout=timeout_in_seconds,
            log_handler=log_handler,
        )
        exploitation_test.run()

        TestMonkeyBlackbox.assert_depth_restriction(
            agents=exploitation_test.agents,
            configured_depth=test_configuration.agent_configuration.propagation.maximum_depth,
        )

    @staticmethod
    def get_log_dir_path():
        return os.path.abspath(LOG_DIR_PATH)

    def test_credentials_reuse_ssh_key(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, credentials_reuse_ssh_key_test_configuration, "Credentials_Reuse_SSH_Key"
        )

    def test_depth_2_a(self, island_client):
        test_name = "Depth2A test suite"

        communication_analyzer = CommunicationAnalyzer(
            island_client,
            get_target_ips(depth_2_a_test_configuration),
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )

        stolen_credentials_analyzer = StolenCredentialsAnalyzer(
            island_client, expected_credentials_depth_2_a
        )
        exploitation_test = ExploitationTest(
            name=test_name,
            island_client=island_client,
            test_configuration=depth_2_a_test_configuration,
            masque=None,
            analyzers=[communication_analyzer, stolen_credentials_analyzer],
            timeout=DEFAULT_TIMEOUT_SECONDS + 30,
            log_handler=log_handler,
        )
        exploitation_test.run()

        # asserting that Agent hashes are not unique
        assert len({a.sha256 for a in exploitation_test.agents}) == 2

        TestMonkeyBlackbox.assert_depth_restriction(
            agents=exploitation_test.agents,
            configured_depth=depth_2_a_test_configuration.agent_configuration.propagation.maximum_depth,  # noqa: E501
        )

    def test_depth_1_a(self, island_client):
        test_name = "Depth1A test suite"
        masque = b"m0nk3y"

        communication_analyzer = CommunicationAnalyzer(
            island_client,
            get_target_ips(depth_1_a_test_configuration),
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        stolen_credentials_analyzer = StolenCredentialsAnalyzer(
            island_client, expected_credentials_depth_1_a
        )
        exploitation_test = ExploitationTest(
            name=test_name,
            island_client=island_client,
            test_configuration=depth_1_a_test_configuration,
            masque=masque,
            analyzers=[communication_analyzer, stolen_credentials_analyzer],
            timeout=DEFAULT_TIMEOUT_SECONDS + 30,
            log_handler=log_handler,
        )
        exploitation_test.run()

        TestMonkeyBlackbox.assert_unique_agent_hashes(exploitation_test.agents)
        TestMonkeyBlackbox.assert_depth_restriction(
            agents=exploitation_test.agents,
            configured_depth=depth_1_a_test_configuration.agent_configuration.propagation.maximum_depth,  # noqa: E501
        )

    def test_depth_3_a(self, island_client):
        test_name = "Depth3A test suite"

        communication_analyzer = CommunicationAnalyzer(
            island_client,
            get_target_ips(depth_3_a_test_configuration),
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        exploitation_test = ExploitationTest(
            name=test_name,
            island_client=island_client,
            test_configuration=depth_3_a_test_configuration,
            masque=None,
            analyzers=[communication_analyzer],
            timeout=DEFAULT_TIMEOUT_SECONDS,
            log_handler=log_handler,
        )
        exploitation_test.run()

        TestMonkeyBlackbox.assert_unique_agent_hashes(exploitation_test.agents)
        TestMonkeyBlackbox.assert_depth_restriction(
            agents=exploitation_test.agents,
            configured_depth=depth_3_a_test_configuration.agent_configuration.propagation.maximum_depth,  # noqa: E501
        )

    def test_depth_4_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, depth_4_a_test_configuration, "Depth4A test suite", masque=b"m0nk3y"
        )

    # Not grouped because it's slow
    def test_zerologon_exploiter(self, island_client):
        test_name = "Zerologon_exploiter"

        expected_creds = [
            "Administrator",
            "aad3b435b51404eeaad3b435b51404ee",
            "2864b62ea4496934a5d6e86f50b834a5",
        ]

        zero_logon_analyzer = ZerologonAnalyzer(island_client, expected_creds)
        communication_analyzer = CommunicationAnalyzer(
            island_client,
            get_target_ips(zerologon_test_configuration),
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        exploitation_test = ExploitationTest(
            name=test_name,
            island_client=island_client,
            test_configuration=zerologon_test_configuration,
            masque=b"",
            analyzers=[zero_logon_analyzer, communication_analyzer],
            timeout=DEFAULT_TIMEOUT_SECONDS + 30,
            log_handler=log_handler,
        )
        exploitation_test.run()

        TestMonkeyBlackbox.assert_depth_restriction(
            agents=exploitation_test.agents,
            configured_depth=zerologon_test_configuration.agent_configuration.propagation.maximum_depth,  # noqa: E501
        )

    # Not grouped because it's depth 1 but conflicts with SMB exploiter in group depth_1_a
    def test_smb_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, smb_pth_test_configuration, "SMB_PTH"
        )
