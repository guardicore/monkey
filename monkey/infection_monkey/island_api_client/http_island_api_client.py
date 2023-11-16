import functools
import json
import logging
from pprint import pformat
from time import sleep
from typing import Any, Dict, List, Sequence

import requests
from egg_timer import EggTimer
from monkeyevents import AbstractAgentEvent
from monkeytypes import (
    OTP,
    AgentID,
    AgentPluginManifest,
    AgentPluginType,
    BasicLock,
    Credentials,
    JSONSerializable,
    OperatingSystem,
)
from requests import Response

from common import AgentHeartbeat, AgentRegistrationData, AgentSignals
from common.agent_configuration import AgentConfiguration
from common.agent_event_serializers import AgentEventSerializerRegistry
from common.agent_plugins import AgentPlugin
from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, TOKEN_TTL_KEY_NAME

from . import IIslandAPIClient, IslandAPIRequestError
from .http_client import HTTPClient
from .island_api_client_errors import (
    IslandAPIAuthenticationError,
    IslandAPIRequestLimitExceededError,
    IslandAPIResponseParsingError,
)

logger = logging.getLogger(__name__)

# After 85% of the token's TTL has expired, it should be refreshed.
TOKEN_TTL_FACTOR = 0.85


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


def handle_authentication_token_expiration(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        with self._token_refresh_lock:
            if self._token_timer.is_expired():
                logger.debug(
                    "The authentication token is close to expiring - refreshing the token before "
                    "making the requested API call..."
                )
                self._refresh_token()

            return fn(self, *args, **kwargs)

    return wrapper


class HTTPIslandAPIClient(IIslandAPIClient):
    """
    A client for the Island's HTTP API
    """

    TOKEN_HEADER_KEY = "Authentication-Token"

    def __init__(
        self,
        agent_event_serializer_registry: AgentEventSerializerRegistry,
        http_client: HTTPClient,
        agent_id: AgentID,
        token_refresh_lock: BasicLock,
    ):
        self._agent_event_serializer_registry = agent_event_serializer_registry
        self._http_client = http_client
        self._agent_id = agent_id
        self._token_timer = EggTimer()
        self._token_refresh_lock = token_refresh_lock

    @handle_response_parsing_errors
    def login(self, otp: OTP):
        try:
            response = self._http_client.post(
                "/agent-otp-login", {"agent_id": str(self._agent_id), "otp": otp.get_secret_value()}
            )
            self._update_token_from_response(response)
        except Exception:
            # We need to catch all exceptions here because we don't want to leak the OTP
            raise IslandAPIAuthenticationError(
                "HTTPIslandAPIClient failed to authenticate to the Island."
            )

    def _update_token_from_response(self, response: Response):
        token_in_response = response.json()["response"]["user"]
        auth_token = token_in_response[ACCESS_TOKEN_KEY_NAME]
        token_ttl_sec = token_in_response[TOKEN_TTL_KEY_NAME]

        self._http_client.additional_headers[HTTPIslandAPIClient.TOKEN_HEADER_KEY] = auth_token
        self._token_timer.set(token_ttl_sec * TOKEN_TTL_FACTOR)

    @handle_response_parsing_errors
    def logout(self):
        self._http_client.post("/logout")

    @handle_response_parsing_errors
    def _refresh_token(self):
        for _ in range(6):
            try:
                response = self._http_client.post("/refresh-authentication-token", {})
                self._update_token_from_response(response)
                break
            except IslandAPIRequestLimitExceededError:
                sleep(0.5)
                continue

    @handle_authentication_token_expiration
    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        os_name = operating_system.value
        response = self._http_client.get(f"/agent-binaries/{os_name}")
        return response.content

    @handle_response_parsing_errors
    @handle_authentication_token_expiration
    def get_otp(self) -> str:
        response = self._http_client.get("/agent-otp")
        return response.json()["otp"]

    @handle_response_parsing_errors
    @handle_authentication_token_expiration
    def get_agent_plugin(
        self, operating_system: OperatingSystem, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPlugin:
        response = self._http_client.get(
            f"/agent-plugins/{operating_system.value}/{plugin_type.value}/{plugin_name}"
        )

        return AgentPlugin(**response.json())

    @handle_response_parsing_errors
    @handle_authentication_token_expiration
    def get_agent_plugin_manifest(
        self, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPluginManifest:
        response = self._http_client.get(
            f"/agent-plugins/{plugin_type.value}/{plugin_name}/manifest"
        )

        return AgentPluginManifest(**response.json())

    @handle_response_parsing_errors
    @handle_authentication_token_expiration
    def get_agent_signals(self) -> AgentSignals:
        response = self._http_client.get(
            f"/agent-signals/{self._agent_id}", timeout=SHORT_REQUEST_TIMEOUT
        )

        return AgentSignals(**response.json())

    @handle_response_parsing_errors
    @handle_authentication_token_expiration
    def get_agent_configuration_schema(self) -> Dict[str, Any]:
        response = self._http_client.get(
            "/agent-configuration-schema", timeout=SHORT_REQUEST_TIMEOUT
        )
        schema = response.json()

        return schema

    @handle_response_parsing_errors
    @handle_authentication_token_expiration
    def get_config(self) -> AgentConfiguration:
        response = self._http_client.get("/agent-configuration", timeout=SHORT_REQUEST_TIMEOUT)

        config_dict = response.json()
        logger.debug(f"Received configuration:\n{pformat(config_dict, sort_dicts=False)}")

        return AgentConfiguration(**config_dict)

    @handle_response_parsing_errors
    @handle_authentication_token_expiration
    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        response = self._http_client.get("/propagation-credentials", timeout=SHORT_REQUEST_TIMEOUT)

        return [Credentials(**credentials) for credentials in response.json()]

    @handle_authentication_token_expiration
    def register_agent(self, agent_registration_data: AgentRegistrationData):
        self._http_client.post(
            "/agents",
            agent_registration_data.to_json_dict(),
            SHORT_REQUEST_TIMEOUT,
        )

    @handle_authentication_token_expiration
    def send_events(self, events: Sequence[AbstractAgentEvent]):
        self._http_client.post("/agent-events", self._serialize_events(events))

    def _serialize_events(self, events: Sequence[AbstractAgentEvent]) -> JSONSerializable:
        serialized_events: List[JSONSerializable] = []

        try:
            for e in events:
                serializer = self._agent_event_serializer_registry[e.__class__]
                serialized_events.append(serializer.serialize(e))
        except Exception as err:
            raise IslandAPIRequestError(err)

        return serialized_events

    @handle_authentication_token_expiration
    def send_heartbeat(self, timestamp: float):
        data = AgentHeartbeat(timestamp=timestamp).to_json_dict()  # type: ignore [arg-type]
        self._http_client.post(f"/agent/{self._agent_id}/heartbeat", data)

    @handle_authentication_token_expiration
    def send_log(self, log_contents: str):
        self._http_client.put(
            f"/agent-logs/{self._agent_id}",
            log_contents,
        )

    def terminate_signal_is_set(self) -> bool:
        agent_signals = self.get_agent_signals()
        return agent_signals.terminate is not None
