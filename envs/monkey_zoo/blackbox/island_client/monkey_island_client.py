import json
import logging
import time
from http import HTTPStatus
from threading import Thread
from typing import Any, Dict, List, Mapping, Optional, Sequence

from monkeytype import AgentPluginType

from common import OperatingSystem
from common.agent_plugins import AgentPluginRepositoryIndex
from common.credentials import Credentials
from common.types import AgentID, MachineID
from envs.monkey_zoo.blackbox.island_client.i_monkey_island_requests import IMonkeyIslandRequests
from envs.monkey_zoo.blackbox.test_configurations.test_configuration import TestConfiguration
from monkey_island.cc.models import Agent, Machine, TerminateAllAgents

SLEEP_BETWEEN_REQUESTS_SECONDS = 0.5
GET_AGENTS_ENDPOINT = "api/agents"
GET_LOG_ENDPOINT = "api/agent-logs"
ISLAND_LOG_ENDPOINT = "api/island/log"
GET_MACHINES_ENDPOINT = "api/machines"
GET_AGENT_EVENTS_ENDPOINT = "api/agent-events"
LOGOUT_ENDPOINT = "api/logout"
GET_AGENT_OTP_ENDPOINT = "/api/agent-otp"
INSTALL_PLUGIN_URL = "api/install-agent-plugin"

logger = logging.getLogger(__name__)


def avoid_race_condition(func):
    time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
    return func


class MonkeyIslandClient(object):
    def __init__(self, requests: IMonkeyIslandRequests):
        self.requests = requests

    def get_api_status(self):
        return self.requests.get("api")

    def install_agent_plugins(self):
        available_plugins_index_url = "api/agent-plugins/available/index"
        installed_plugins_manifests_url = "api/agent-plugins/installed/manifests"

        response = self.requests.get(available_plugins_index_url)
        plugin_repository_index = AgentPluginRepositoryIndex(**response.json())

        response = self.requests.get(installed_plugins_manifests_url)
        installed_plugins = response.json()

        install_threads: List[Thread] = []

        # all of the responses from the API endpoints are serialized
        # so we don't need to worry about type conversion
        for plugin_type in plugin_repository_index.plugins:
            install_threads.extend(
                self._install_all_agent_plugins_of_type(
                    plugin_type, plugin_repository_index, installed_plugins
                )
            )

        for t in install_threads:
            t.join()

    def _install_all_agent_plugins_of_type(
        self,
        plugin_type: AgentPluginType,
        plugin_repository_index: AgentPluginRepositoryIndex,
        installed_plugins: Dict[str, Any],
    ) -> Sequence[Thread]:
        logger.info(f"Installing {plugin_type} plugins")
        install_threads: List[Thread] = []
        for plugin_name in plugin_repository_index.plugins[plugin_type]:
            plugin_versions = plugin_repository_index.plugins[plugin_type][plugin_name]
            latest_version = str(plugin_versions[-1].version)

            if self._latest_version_already_installed(
                installed_plugins, plugin_type, plugin_name, latest_version
            ):
                logger.info(f"{plugin_type}-{plugin_name}-v{latest_version} is already installed")
                continue

            t = Thread(
                target=self._install_single_agent_plugin,
                args=(plugin_name, plugin_type, latest_version),
                daemon=True,
            )
            t.start()
            install_threads.append(t)

        return install_threads

    def _latest_version_already_installed(
        self,
        installed_plugins: Dict[str, Any],
        plugin_type: AgentPluginType,
        plugin_name: str,
        latest_version: str,
    ) -> bool:
        installed_plugin = installed_plugins.get(plugin_type, {}).get(plugin_name, {})
        return installed_plugin and installed_plugin.get("version", "") == latest_version

    def _install_single_agent_plugin(
        self,
        plugin_name: str,
        plugin_type: AgentPluginType,
        latest_version: str,
    ):
        install_plugin_request = {
            "plugin_type": plugin_type,
            "name": plugin_name,
            "version": latest_version,
        }
        if self.requests.put_json(url=INSTALL_PLUGIN_URL, json=install_plugin_request).ok:
            logger.info(f"Installed {plugin_name} {plugin_type} v{latest_version} to Island")
        else:
            logger.error(
                f"Could not install {plugin_name} {plugin_type} " f"v{latest_version} to Island"
            )

    @avoid_race_condition
    def set_masque(self, masque):
        masque = b"" if masque is None else masque
        for operating_system in [operating_system.name for operating_system in OperatingSystem]:
            if self.requests.put(f"api/agent-binaries/{operating_system}/masque", data=masque).ok:
                formatted_masque = masque if len(masque) <= 64 else (masque[:64] + b"...")
                logger.info(f'Setting {operating_system} masque to "{formatted_masque}"')
            else:
                logger.error(f"Failed to set {operating_system} masque")
                assert False

    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        response = self.requests.get(f"api/agent-binaries/{operating_system.name}")
        return response.content

    def get_propagation_credentials(self) -> Sequence[Credentials]:
        response = self.requests.get("api/propagation-credentials")
        return [Credentials(**credentials) for credentials in response.json()]

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        response = self.requests.get("api/propagation-credentials/stolen-credentials")
        return [Credentials(**credentials) for credentials in response.json()]

    @avoid_race_condition
    def import_config(self, test_configuration: TestConfiguration):
        self._import_config(test_configuration)
        self._import_credentials(test_configuration.propagation_credentials)

    @avoid_race_condition
    def _import_config(self, test_configuration: TestConfiguration):
        response = self.requests.put_json(
            "api/agent-configuration",
            json=test_configuration.agent_configuration.dict(simplify=True),
        )
        if response.ok:
            logger.info("Configuration is imported.")
        else:
            logger.error(f"Failed to import config: {response}")
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
            logger.info("Credentials are imported.")
        else:
            logger.error(f"Failed to import credentials: {response}")
            assert False

    @avoid_race_condition
    def run_monkey_local(self):
        response = self.requests.post_json("api/local-monkey", json={"action": "run"})
        if MonkeyIslandClient.monkey_ran_successfully(response):
            logger.info("Running the monkey.")
        else:
            logger.error("Failed to run the monkey.")
            assert False

    @staticmethod
    def monkey_ran_successfully(response):
        return response.ok and json.loads(response.content)["is_running"]

    @avoid_race_condition
    def kill_all_monkeys(self):
        # TODO change this request, because monkey-control resource got removed
        response = self.requests.post_json(
            "api/agent-signals/terminate-all-agents",
            json=TerminateAllAgents(timestamp=time.time()).dict(simplify=True),
        )
        if response.ok:
            logger.info("Killing all monkeys after the test.")
        else:
            logger.error("Failed to kill all monkeys.")
            logger.error(response.status_code)
            logger.error(response.content)
            assert False

    @avoid_race_condition
    def reset_island(self):
        self._reset_agent_configuration()
        self._reset_simulation_data()
        self._reset_credentials()
        self.set_masque(b"")

    def _reset_agent_configuration(self):
        if self.requests.post("api/reset-agent-configuration", data=None).ok:
            logger.info("Resetting agent-configuration after the test.")
        else:
            logger.error("Failed to reset agent configuration.")
            assert False

    def _reset_simulation_data(self):
        if self.requests.post("api/clear-simulation-data", data=None).ok:
            logger.info("Clearing simulation data.")
        else:
            logger.error("Failed to clear simulation data")
            assert False

    def _reset_credentials(self):
        if self.requests.put_json("api/propagation-credentials/configured-credentials", json=[]).ok:
            logger.info("Resseting configured credentials after the test.")
        else:
            logger.error("Failed to reset configured credentials")
            assert False

    def get_agents(self) -> Sequence[Agent]:
        response = self.requests.get(GET_AGENTS_ENDPOINT)

        return [Agent(**a) for a in response.json()]

    def get_machines(self) -> Mapping[MachineID, Machine]:
        response = self.requests.get(GET_MACHINES_ENDPOINT)
        machines = (Machine(**m) for m in response.json())

        return {m.id: m for m in machines}

    def get_agent_log(self, agent_id: AgentID) -> Optional[str]:
        response = self.requests.get(f"{GET_LOG_ENDPOINT}/{agent_id}")

        if response.status_code == HTTPStatus.NOT_FOUND:
            logger.error(f"No log found for agent: {agent_id}")
            return None
        else:
            response.raise_for_status()

        return response.json()

    def get_island_log(self):
        response = self.requests.get(f"{ISLAND_LOG_ENDPOINT}")

        response.raise_for_status()

        return response.json()

    def get_agent_events(self):
        response = self.requests.get(GET_AGENT_EVENTS_ENDPOINT)

        return response.json()

    def is_all_monkeys_dead(self):
        agents = self.get_agents()
        return all((a.stop_time is not None for a in agents))

    def register(self):
        try:
            self.requests.register()
            logger.info("Successfully registered a user with the Island.")
        except Exception:
            logger.error("Failed to register a user with the Island.")

    def login(self):
        try:
            self.requests.login()
            logger.info("Logged into the Island.")
        except Exception:
            logger.error("Failed to log into the Island.")
            assert False

    def logout(self):
        if self.requests.post(LOGOUT_ENDPOINT, data=None).ok:
            logger.info("Logged out of the Island.")
        else:
            logger.error("Failed to log out of the Island.")
            assert False

    def get_agent_otp(self):
        response = self.requests.get(GET_AGENT_OTP_ENDPOINT)
        return response.json()
