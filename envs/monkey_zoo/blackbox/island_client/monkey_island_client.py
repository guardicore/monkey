import json
import logging
import time
from typing import List, Mapping, Sequence, Union

from bson import json_util

from common.credentials import Credentials
from common.types import MachineID
from envs.monkey_zoo.blackbox.island_client.monkey_island_requests import MonkeyIslandRequests
from envs.monkey_zoo.blackbox.test_configurations.test_configuration import TestConfiguration
from monkey_island.cc.models import Agent, Machine

SLEEP_BETWEEN_REQUESTS_SECONDS = 0.5
GET_AGENTS_ENDPOINT = "api/agents"
GET_MACHINES_ENDPOINT = "api/machines"
MONKEY_TEST_ENDPOINT = "api/test/monkey"
TELEMETRY_TEST_ENDPOINT = "api/test/telemetry"
LOG_TEST_ENDPOINT = "api/test/log"
LOGGER = logging.getLogger(__name__)


def avoid_race_condition(func):
    time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
    return func


class MonkeyIslandClient(object):
    def __init__(self, server_address):
        self.requests = MonkeyIslandRequests(server_address)

    def get_api_status(self):
        return self.requests.get("api")

    def get_propagation_credentials(self) -> Sequence[Credentials]:
        response = self.requests.get("api/propagation-credentials")
        return [Credentials(**credentials) for credentials in response.json()]

    @avoid_race_condition
    def import_config(self, test_configuration: TestConfiguration):
        self._set_island_mode()
        self._import_config(test_configuration)
        self._import_credentials(test_configuration.propagation_credentials)

    @avoid_race_condition
    def _set_island_mode(self):
        if self.requests.put_json("api/island/mode", json="advanced").ok:
            LOGGER.info("Setting island mode to Custom.")
        else:
            LOGGER.error("Failed to set island mode")
            assert False

    @avoid_race_condition
    def _import_config(self, test_configuration: TestConfiguration):
        response = self.requests.put_json(
            "api/agent-configuration",
            json=test_configuration.agent_configuration.dict(simplify=True),
        )
        if response.ok:
            LOGGER.info("Configuration is imported.")
        else:
            LOGGER.error(f"Failed to import config: {response}")
            assert False

    @avoid_race_condition
    def _import_credentials(self, propagation_credentials: List[Credentials]):
        serialized_propagation_credentials = [
            credentials.dict(simplify=True) for credentials in propagation_credentials
        ]
        response = self.requests.put_json(
            "/api/propagation-credentials/configured-credentials",
            json=serialized_propagation_credentials,
        )
        if response.ok:
            LOGGER.info("Credentials are imported.")
        else:
            LOGGER.error(f"Failed to import credentials: {response}")
            assert False

    @avoid_race_condition
    def run_monkey_local(self):
        response = self.requests.post_json("api/local-monkey", json={"action": "run"})
        if MonkeyIslandClient.monkey_ran_successfully(response):
            LOGGER.info("Running the monkey.")
        else:
            LOGGER.error("Failed to run the monkey.")
            assert False

    @staticmethod
    def monkey_ran_successfully(response):
        return response.ok and json.loads(response.content)["is_running"]

    @avoid_race_condition
    def kill_all_monkeys(self):
        # TODO change this request, because monkey-control resource got removed
        response = self.requests.post_json(
            "api/agent-signals/terminate-all-agents", json={"terminate_time": time.time()}
        )
        if response.ok:
            LOGGER.info("Killing all monkeys after the test.")
        else:
            LOGGER.error("Failed to kill all monkeys.")
            LOGGER.error(response.status_code)
            LOGGER.error(response.content)
            assert False

    @avoid_race_condition
    def reset_island(self):
        self._reset_agent_configuration()
        self._reset_simulation_data()
        self._reset_credentials()
        self._reset_island_mode()

    def _reset_agent_configuration(self):
        if self.requests.post("api/reset-agent-configuration", data=None).ok:
            LOGGER.info("Resetting agent-configuration after the test.")
        else:
            LOGGER.error("Failed to reset agent configuration.")
            assert False

    def _reset_simulation_data(self):
        if self.requests.post("api/clear-simulation-data", data=None).ok:
            LOGGER.info("Clearing simulation data.")
        else:
            LOGGER.error("Failed to clear simulation data")
            assert False

    def _reset_credentials(self):
        if self.requests.put_json("api/propagation-credentials/configured-credentials", json=[]).ok:
            LOGGER.info("Resseting configured credentials after the test.")
        else:
            LOGGER.error("Failed to reset configured credentials")
            assert False

    def _reset_island_mode(self):
        if self.requests.put_json("api/island/mode", json="unset").ok:
            LOGGER.info("Resetting island mode after the test.")
        else:
            LOGGER.error("Failed to reset island mode")
            assert False

    def find_monkeys_in_db(self, query):
        if query is None:
            raise TypeError
        response = self.requests.get(
            MONKEY_TEST_ENDPOINT, MonkeyIslandClient.form_find_query_for_request(query)
        )
        return MonkeyIslandClient.get_test_query_results(response)

    def find_telems_in_db(self, query: dict):
        if query is None:
            raise TypeError
        response = self.requests.get(
            TELEMETRY_TEST_ENDPOINT, MonkeyIslandClient.form_find_query_for_request(query)
        )
        return MonkeyIslandClient.get_test_query_results(response)

    def get_all_monkeys_from_db(self):
        response = self.requests.get(
            MONKEY_TEST_ENDPOINT, MonkeyIslandClient.form_find_query_for_request(None)
        )
        return MonkeyIslandClient.get_test_query_results(response)

    def get_agents(self) -> Sequence[Agent]:
        response = self.requests.get(GET_AGENTS_ENDPOINT)

        return [Agent(**a) for a in response.json()]

    def get_machines(self) -> Mapping[MachineID, Machine]:
        response = self.requests.get(GET_MACHINES_ENDPOINT)
        machines = (Machine(**m) for m in response.json())

        return {m.id: m for m in machines}

    def find_log_in_db(self, query):
        response = self.requests.get(
            LOG_TEST_ENDPOINT, MonkeyIslandClient.form_find_query_for_request(query)
        )
        return MonkeyIslandClient.get_test_query_results(response)

    @staticmethod
    def form_find_query_for_request(query: Union[dict, None]) -> dict:
        return {"find_query": json_util.dumps(query)}

    @staticmethod
    def get_test_query_results(response):
        return json.loads(response.content)["results"]

    def is_all_monkeys_dead(self):
        query = {"dead": False}
        return len(self.find_monkeys_in_db(query)) == 0
