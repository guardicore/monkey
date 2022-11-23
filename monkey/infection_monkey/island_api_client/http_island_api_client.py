import functools
import json
import logging
from pprint import pformat
from typing import List, Sequence

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from common import AgentRegistrationData, AgentSignals, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_event_serializers import AgentEventSerializerRegistry
from common.agent_events import AbstractAgentEvent
from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT, SHORT_REQUEST_TIMEOUT
from common.credentials import Credentials
from common.types import AgentID, JSONSerializable, PluginType, SocketAddress

from . import (
    AbstractIslandAPIClientFactory,
    IIslandAPIClient,
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
)

logger = logging.getLogger(__name__)

# Retries improve reliability and slightly mitigates performance issues
RETRIES = 5


def handle_island_errors(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except IslandAPIError as err:
            raise err
        except (requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects) as err:
            raise IslandAPIConnectionError(err)
        except requests.exceptions.HTTPError as err:
            if 400 <= err.response.status_code < 500:
                raise IslandAPIRequestError(err)
            elif 500 <= err.response.status_code < 600:
                raise IslandAPIRequestFailedError(err)
            else:
                raise IslandAPIError(err)
        except TimeoutError as err:
            raise IslandAPITimeoutError(err)
        except Exception as err:
            raise IslandAPIError(err)

    return decorated


def convert_json_error_to_island_api_error(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except (requests.JSONDecodeError, json.JSONDecodeError) as err:
            raise IslandAPIRequestFailedError(err)

    return wrapper


class HTTPIslandAPIClient(IIslandAPIClient):
    """
    A client for the Island's HTTP API
    """

    def __init__(
        self,
        agent_event_serializer_registry: AgentEventSerializerRegistry,
        retries=RETRIES,
    ):
        self._agent_event_serializer_registry = agent_event_serializer_registry
        self._session = requests.Session()
        retry_config = Retry(retries)
        self._session.mount("https://", HTTPAdapter(max_retries=retry_config))

    @handle_island_errors
    def connect(
        self,
        island_server: SocketAddress,
    ):
        response = self._session.get(  # noqa: DUO123
            f"https://{island_server}/api?action=is-up",
            verify=False,
            timeout=MEDIUM_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        self._api_url = f"https://{island_server}/api"

    def _get(self, endpoint: str, timeout: float) -> requests.Response:
        url = f"{self._api_url}/{endpoint}"
        logger.debug(f"GET {url}, timeout={timeout}")

        return self._session.get(url, verify=False, timeout=timeout)  # noqa: DUO123

    def _post(self, endpoint: str, data: JSONSerializable, timeout: float) -> requests.Response:
        url = f"{self._api_url}/{endpoint}"
        logger.debug(f"POST {url}, timeout={timeout}")

        return self._session.post(url, json=data, verify=False, timeout=timeout)  # noqa: DUO123

    def _put(self, endpoint: str, data: JSONSerializable, timeout: float) -> requests.Response:
        url = f"{self._api_url}/{endpoint}"
        logger.debug(f"PUT {url}, timeout={timeout}")

        return self._session.put(url, json=data, verify=False, timeout=timeout)  # noqa: DUO123

    @handle_island_errors
    def send_log(self, agent_id: AgentID, log_contents: str):
        response = self._put(f"agent-logs/{agent_id}", log_contents, MEDIUM_REQUEST_TIMEOUT)
        response.raise_for_status()

    @handle_island_errors
    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        os_name = operating_system.value
        response = self._get(f"agent-binaries/{os_name}", MEDIUM_REQUEST_TIMEOUT)
        response.raise_for_status()

        return response.content

    @handle_island_errors
    def send_events(self, events: Sequence[AbstractAgentEvent]):
        response = self._post(
            "agent-events", self._serialize_events(events), MEDIUM_REQUEST_TIMEOUT
        )
        response.raise_for_status()

    @handle_island_errors
    def register_agent(self, agent_registration_data: AgentRegistrationData):
        response = self._post(
            "agents", agent_registration_data.dict(simplify=True), SHORT_REQUEST_TIMEOUT
        )
        response.raise_for_status()

    @handle_island_errors
    @convert_json_error_to_island_api_error
    def get_config(self) -> AgentConfiguration:
        response = self._get("agent-configuration", SHORT_REQUEST_TIMEOUT)
        response.raise_for_status()

        config_dict = response.json()
        logger.debug(f"Received configuration:\n{pformat(config_dict)}")

        return AgentConfiguration(**config_dict)

    @handle_island_errors
    @convert_json_error_to_island_api_error
    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        response = self._get("propagation-credentials", SHORT_REQUEST_TIMEOUT)
        response.raise_for_status()

        return [Credentials(**credentials) for credentials in response.json()]

    def _serialize_events(self, events: Sequence[AbstractAgentEvent]) -> JSONSerializable:
        serialized_events: List[JSONSerializable] = []

        try:
            for e in events:
                serializer = self._agent_event_serializer_registry[e.__class__]
                serialized_events.append(serializer.serialize(e))
        except Exception as err:
            raise IslandAPIRequestError(err)

        return serialized_events

    @handle_island_errors
    @convert_json_error_to_island_api_error
    def get_agent_signals(self, agent_id: str) -> AgentSignals:
        response = self._get(f"agent-signals/{agent_id}", SHORT_REQUEST_TIMEOUT)
        response.raise_for_status()

        return AgentSignals(**response.json())

    @handle_island_errors
    def get_plugin(self, plugin_type: PluginType, plugin_name: str) -> bytes:
        response = self._get(
            f"/api/agent-plugins/{plugin_type.value}/{plugin_name}", MEDIUM_REQUEST_TIMEOUT
        )

        return response.content


class HTTPIslandAPIClientFactory(AbstractIslandAPIClientFactory):
    def __init__(
        self,
        agent_event_serializer_registry: AgentEventSerializerRegistry,
    ):
        self._agent_event_serializer_registry = agent_event_serializer_registry

    def create_island_api_client(self) -> IIslandAPIClient:
        return HTTPIslandAPIClient(self._agent_event_serializer_registry)
