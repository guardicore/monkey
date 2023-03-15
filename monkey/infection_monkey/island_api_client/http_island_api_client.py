import functools
import json
import logging
from pprint import pformat
from typing import Any, Dict, List, Sequence

import requests

from common import AgentHeartbeat, AgentRegistrationData, AgentSignals, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_event_serializers import AgentEventSerializerRegistry
from common.agent_events import AbstractAgentEvent
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from common.credentials import Credentials
from common.types import AgentID, JSONSerializable, SocketAddress

from . import IIslandAPIClient, IslandAPIRequestError
from .http_client import HTTPClient
from .island_api_client_errors import IslandAPIResponseParsingError, UnconnectedClientError

logger = logging.getLogger(__name__)


def handle_response_parsing_errors(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except (
            requests.exceptions.JSONDecodeError,
            json.JSONDecodeError,
            ValueError,
            TypeError,
            KeyError,
        ) as err:
            raise IslandAPIResponseParsingError(err)

    return wrapper


def ensure_client_connected(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self.http_client is not None:
            return fn(self, *args, **kwargs)
        else:
            raise UnconnectedClientError(
                f"The client can't {fn.__name__}" f" because it's not connected to any server."
            )

    return wrapper


class HTTPIslandAPIClient(IIslandAPIClient):
    """
    A client for the Island's HTTP API
    """

    def __init__(
        self,
        agent_event_serializer_registry: AgentEventSerializerRegistry,
        http_client: HTTPClient,
        otp: str,
    ):
        self._agent_event_serializer_registry = agent_event_serializer_registry
        self.http_client = http_client
        self._otp = otp

    def connect(
        self,
        island_server: SocketAddress,
    ):
        try:
            self.http_client.server_url = f"{island_server}/api"
            self.http_client.get("?action=is-up")
        except Exception as err:
            logger.debug(f"Connection to {island_server} failed: {err}")
            self.http_client.server_url = None
            raise err

        try:
            auth_token = self._get_authentication_token()
        except Exception as err:
            logger.debug("Authentication failed")
            raise err

        self.http_client.additional_headers = {"Authentication-Token": auth_token}

    def _get_authentication_token(self) -> str:
        response = self.http_client.post("/agent-otp-login", {"otp": self._otp})
        return response.json()["token"]

    @ensure_client_connected
    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        os_name = operating_system.value
        response = self.http_client.get(f"/agent-binaries/{os_name}")
        return response.content

    @handle_response_parsing_errors
    def get_otp(self) -> str:
        response = self.http_client.get("/agent-otp")
        return response.json()["otp"]

    @ensure_client_connected
    @handle_response_parsing_errors
    def get_agent_plugin(
        self, operating_system: OperatingSystem, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPlugin:
        response = self.http_client.get(
            f"/agent-plugins/{operating_system.value}/{plugin_type.value}/{plugin_name}"
        )

        return AgentPlugin(**response.json())

    @ensure_client_connected
    @handle_response_parsing_errors
    def get_agent_plugin_manifest(
        self, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPluginManifest:
        response = self.http_client.get(
            f"/agent-plugins/{plugin_type.value}/{plugin_name}/manifest"
        )

        return AgentPluginManifest(**response.json())

    @ensure_client_connected
    @handle_response_parsing_errors
    def get_agent_signals(self, agent_id: str) -> AgentSignals:
        response = self.http_client.get(f"/agent-signals/{agent_id}", timeout=SHORT_REQUEST_TIMEOUT)

        return AgentSignals(**response.json())

    @ensure_client_connected
    @handle_response_parsing_errors
    def get_agent_configuration_schema(self) -> Dict[str, Any]:
        response = self.http_client.get(
            "/agent-configuration-schema", timeout=SHORT_REQUEST_TIMEOUT
        )
        schema = response.json()

        return schema

    @ensure_client_connected
    @handle_response_parsing_errors
    def get_config(self) -> AgentConfiguration:
        response = self.http_client.get("/agent-configuration", timeout=SHORT_REQUEST_TIMEOUT)

        config_dict = response.json()
        logger.debug(f"Received configuration:\n{pformat(config_dict, sort_dicts=False)}")

        return AgentConfiguration(**config_dict)

    @ensure_client_connected
    @handle_response_parsing_errors
    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        response = self.http_client.get("/propagation-credentials", timeout=SHORT_REQUEST_TIMEOUT)

        return [Credentials(**credentials) for credentials in response.json()]

    @ensure_client_connected
    def register_agent(self, agent_registration_data: AgentRegistrationData):
        self.http_client.post(
            "/agents",
            agent_registration_data.dict(simplify=True),
            SHORT_REQUEST_TIMEOUT,
        )

    @ensure_client_connected
    def send_events(self, events: Sequence[AbstractAgentEvent]):
        self.http_client.post("/agent-events", self._serialize_events(events))

    def _serialize_events(self, events: Sequence[AbstractAgentEvent]) -> JSONSerializable:
        serialized_events: List[JSONSerializable] = []

        try:
            for e in events:
                serializer = self._agent_event_serializer_registry[e.__class__]
                serialized_events.append(serializer.serialize(e))
        except Exception as err:
            raise IslandAPIRequestError(err)

        return serialized_events

    @ensure_client_connected
    def send_heartbeat(self, agent_id: AgentID, timestamp: float):
        data = AgentHeartbeat(timestamp=timestamp).dict(simplify=True)
        self.http_client.post(f"/agent/{agent_id}/heartbeat", data)

    @ensure_client_connected
    def send_log(self, agent_id: AgentID, log_contents: str):
        self.http_client.put(
            f"/agent-logs/{agent_id}",
            log_contents,
        )
