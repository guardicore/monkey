import functools
import json
import logging
from pprint import pformat
from typing import List, Sequence

import requests

from common import AgentHeartbeat, AgentRegistrationData, AgentSignals, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_event_serializers import AgentEventSerializerRegistry
from common.agent_events import AbstractAgentEvent
from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from common.credentials import Credentials
from common.types import AgentID, JSONSerializable, PluginType, SocketAddress

from . import AbstractIslandAPIClientFactory, IIslandAPIClient, IslandAPIRequestError
from .http_client import HTTPClient
from .island_api_client_errors import IslandAPIResponseParsingError

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
        ) as err:
            raise IslandAPIResponseParsingError(err)

    return wrapper


class HTTPIslandAPIClient(IIslandAPIClient):
    """
    A client for the Island's HTTP API
    """

    def __init__(
        self, agent_event_serializer_registry: AgentEventSerializerRegistry, http_client: HTTPClient
    ):
        self._agent_event_serializer_registry = agent_event_serializer_registry
        self.http_client = http_client

    def connect(
        self,
        island_server: SocketAddress,
    ):
        self.http_client.connect(island_server)

    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        os_name = operating_system.value
        response = self.http_client.get(f"agent-binaries/{os_name}")
        return response.content

    def get_agent_plugin(self, plugin_type: PluginType, plugin_name: str) -> bytes:
        response = self.http_client.get(f"/api/agent-plugins/{plugin_type.value}/{plugin_name}")

        return response.content

    @handle_response_parsing_errors
    def get_agent_signals(self, agent_id: str) -> AgentSignals:
        response = self.http_client.get(f"agent-signals/{agent_id}", timeout=SHORT_REQUEST_TIMEOUT)

        return AgentSignals(**response.json())

    @handle_response_parsing_errors
    def get_config(self) -> AgentConfiguration:
        response = self.http_client.get("agent-configuration", timeout=SHORT_REQUEST_TIMEOUT)

        config_dict = response.json()
        logger.debug(f"Received configuration:\n{pformat(config_dict)}")

        return AgentConfiguration(**config_dict)

    @handle_response_parsing_errors
    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        response = self.http_client.get("propagation-credentials", timeout=SHORT_REQUEST_TIMEOUT)

        return [Credentials(**credentials) for credentials in response.json()]

    def register_agent(self, agent_registration_data: AgentRegistrationData):
        self.http_client.post(
            "agents",
            agent_registration_data.dict(simplify=True),
            SHORT_REQUEST_TIMEOUT,
        )

    def send_events(self, events: Sequence[AbstractAgentEvent]):
        self.http_client.post("agent-events", self._serialize_events(events))

    def _serialize_events(self, events: Sequence[AbstractAgentEvent]) -> JSONSerializable:
        serialized_events: List[JSONSerializable] = []

        try:
            for e in events:
                serializer = self._agent_event_serializer_registry[e.__class__]
                serialized_events.append(serializer.serialize(e))
        except Exception as err:
            raise IslandAPIRequestError(err)

        return serialized_events

    def send_heartbeat(self, agent_id: AgentID, timestamp: float):
        data = AgentHeartbeat(timestamp=timestamp).dict(simplify=True)
        self.http_client.post(f"agent/{agent_id}/heartbeat", data)

    def send_log(self, agent_id: AgentID, log_contents: str):
        self.http_client.put(
            f"agent-logs/{agent_id}",
            log_contents,
        )


class HTTPIslandAPIClientFactory(AbstractIslandAPIClientFactory):
    def __init__(
        self,
        agent_event_serializer_registry: AgentEventSerializerRegistry,
    ):
        self._agent_event_serializer_registry = agent_event_serializer_registry

    def create_island_api_client(self) -> IIslandAPIClient:
        return HTTPIslandAPIClient(self._agent_event_serializer_registry, HTTPClient())
