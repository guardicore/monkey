import logging
import os
from http import HTTPStatus
from time import sleep

import pytest

from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import CommunicationAnalyzer
from envs.monkey_zoo.blackbox.analyzers.zerologon_analyzer import ZerologonAnalyzer
from envs.monkey_zoo.blackbox.island_client.i_monkey_island_requests import IMonkeyIslandRequests
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import (
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
    wmi_mimikatz_test_configuration,
    zerologon_test_configuration,
)
from envs.monkey_zoo.blackbox.test_configurations.test_configuration import TestConfiguration
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest
from envs.monkey_zoo.blackbox.utils.gcp_machine_handlers import (
    initialize_gcp_client,
    start_machines,
    stop_machines,
)

DEFAULT_TIMEOUT_SECONDS = 2 * 60 + 30
MACHINE_BOOTUP_WAIT_SECONDS = 30
LOG_DIR_PATH = "./logs"
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="session")
def GCPHandler(request, no_gcp, gcp_machines_to_start):
    if not no_gcp:
        LOGGER.info(f"MACHINES TO START: {gcp_machines_to_start}")

        try:
            initialize_gcp_client()
            start_machines(gcp_machines_to_start)
        except Exception as e:
            LOGGER.error("GCP Handler failed to initialize: %s." % e)
            pytest.exit("Encountered an error while starting GCP machines. Stopping the tests.")
        wait_machine_bootup()

        def fin():
            stop_machines(gcp_machines_to_start)

        request.addfinalizer(fin)


@pytest.fixture(autouse=True, scope="session")
def delete_logs():
    LOGGER.info("Deleting monkey logs before new tests.")
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
        requests = ReauthorizingMonkeyIslandRequests(monkey_island_requests)
        island_client_object = MonkeyIslandClient(requests)
        client_established = island_client_object.get_api_status()
    except Exception:
        logging.exception("Got an exception while trying to establish connection to the Island.")
    finally:
        if not client_established:
            pytest.exit("BB tests couldn't establish communication to the island.")

    yield island_client_object


@pytest.fixture(autouse=True, scope="session")
def register(island_client):
    logging.info("Registering a new user")
    island_client.register()


@pytest.mark.parametrize(
    "authenticated_endpoint",
    [
        GET_AGENTS_ENDPOINT,
        ISLAND_LOG_ENDPOINT,
        GET_MACHINES_ENDPOINT,
    ],
)
def test_logout(island, authenticated_endpoint):
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


# NOTE: These test methods are ordered to give time for the slower zoo machines
# to boot up and finish starting services.
# noinspection PyUnresolvedReferences
class TestMonkeyBlackbox:
    @staticmethod
    def run_exploitation_test(
        island_client: MonkeyIslandClient,
        test_configuration: TestConfiguration,
        test_name: str,
        timeout_in_seconds=DEFAULT_TIMEOUT_SECONDS,
    ):
        analyzer = CommunicationAnalyzer(
            island_client,
            get_target_ips(test_configuration),
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        ExploitationTest(
            name=test_name,
            island_client=island_client,
            test_configuration=test_configuration,
            analyzers=[analyzer],
            timeout=timeout_in_seconds,
            log_handler=log_handler,
        ).run()

    @staticmethod
    def get_log_dir_path():
        return os.path.abspath(LOG_DIR_PATH)

    def test_credentials_reuse_ssh_key(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, credentials_reuse_ssh_key_test_configuration, "Credentials_Reuse_SSH_Key"
        )

    def test_depth_2_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, depth_2_a_test_configuration, "Depth2A test suite"
        )

    def test_depth_1_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, depth_1_a_test_configuration, "Depth1A test suite"
        )

    def test_depth_3_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, depth_3_a_test_configuration, "Depth3A test suite"
        )

    def test_depth_4_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, depth_4_a_test_configuration, "Depth4A test suite"
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
        ExploitationTest(
            name=test_name,
            island_client=island_client,
            test_configuration=zerologon_test_configuration,
            analyzers=[zero_logon_analyzer, communication_analyzer],
            timeout=DEFAULT_TIMEOUT_SECONDS + 30,
            log_handler=log_handler,
        ).run()

    # Not grouped because conflicts with SMB.
    # Consider grouping when more depth 1 exploiters collide with group depth_1_a
    def test_wmi_and_mimikatz_exploiters(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, wmi_mimikatz_test_configuration, "WMI_exploiter,_mimikatz"
        )

    # Not grouped because it's depth 1 but conflicts with SMB exploiter in group depth_1_a
    def test_smb_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, smb_pth_test_configuration, "SMB_PTH"
        )
