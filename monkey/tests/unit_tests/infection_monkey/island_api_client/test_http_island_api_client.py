import json
from datetime import datetime
from http import HTTPStatus
from typing import Dict, List, Optional
from unittest.mock import MagicMock
from uuid import UUID

import pytest
import requests
from tests.common.example_agent_configuration import AGENT_CONFIGURATION
from tests.data_for_tests.otp import TEST_OTP
from tests.data_for_tests.propagation_credentials import CREDENTIALS_DICTS
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import (
    FAKE_AGENT_MANIFEST_DICT,
    FAKE_MANIFEST_OBJECT,
    FAKE_NAME,
)

from common import AgentRegistrationData, AgentSignals, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    PydanticAgentEventSerializer,
)
from common.agent_events import AbstractAgentEvent
from common.agent_plugins import AgentPluginType
from common.base_models import InfectionMonkeyBaseModel
from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, TOKEN_TTL_KEY_NAME
from common.credentials import Credentials
from common.types import SocketAddress
from infection_monkey.island_api_client import (
    HTTPIslandAPIClient,
    IslandAPIError,
    IslandAPIRequestError,
)
from infection_monkey.island_api_client.island_api_client_errors import (
    IslandAPIAuthenticationError,
    IslandAPIRequestLimitExceededError,
    IslandAPIResponseParsingError,
)

SERVER = SocketAddress(ip="1.1.1.1", port=9999)
WINDOWS = "windows"
AGENT_ID = UUID("80988359-a1cd-42a2-9b47-5b94b37cd673")
AGENT_SHA256 = "7f295ebba73b2f549f98b9c35ae588f153283476ac8f087cc75d9c4788795d82"
AGENT_REGISTRATION = AgentRegistrationData(
    id=AGENT_ID,
    machine_hardware_id=1,
    start_time=0,
    parent_id=None,
    cc_server=SERVER,
    network_interfaces=[],
    sha256=AGENT_SHA256,
)

TIMESTAMP = 123456789

ISLAND_URI = f"https://{SERVER}/api?action=is-up"
ISLAND_SEND_LOG_URI = f"https://{SERVER}/api/agent-logs/{AGENT_ID}"
ISLAND_GET_AGENT_BINARY_URI = f"https://{SERVER}/api/agent-binaries/{WINDOWS}"
ISLAND_SEND_EVENTS_URI = f"https://{SERVER}/api/agent-events"
ISLAND_REGISTER_AGENT_URI = f"https://{SERVER}/api/agents"
ISLAND_AGENT_STOP_URI = f"https://{SERVER}/api/monkey-control/needs-to-stop/{AGENT_ID}"
ISLAND_GET_CONFIG_URI = f"https://{SERVER}/api/agent-configuration"
ISLAND_GET_AGENT_CONFIGURATION_SCHEMA_URI = f"https://{SERVER}/api/agent-configuration-schema"
ISLAND_GET_PROPAGATION_CREDENTIALS_URI = f"https://{SERVER}/api/propagation-credentials"
ISLAND_GET_AGENT_SIGNALS = f"https://{SERVER}/api/agent-signals/{AGENT_ID}"
ISLAND_SEND_HEARTBEAT_URI = f"https://{SERVER}/api/agent/{AGENT_ID}/heartbeat"


class Event1(AbstractAgentEvent):
    a: int


class Event2(AbstractAgentEvent):
    b: str


class Event3(AbstractAgentEvent):
    c: int


class AgentConfigurationSchema(InfectionMonkeyBaseModel):
    some_field: str
    other_field: float


def agent_event_serializer_registry():
    agent_event_serializer_registry = AgentEventSerializerRegistry()
    agent_event_serializer_registry[Event1] = PydanticAgentEventSerializer(Event1)
    agent_event_serializer_registry[Event2] = PydanticAgentEventSerializer(Event2)

    return agent_event_serializer_registry


def build_api_client(http_client):
    return HTTPIslandAPIClient(
        agent_event_serializer_registry(), http_client, AGENT_ID, MagicMock()
    )


def _build_client_with_json_response(response):
    client_stub = MagicMock()
    client_stub.get.return_value.json.return_value = response
    return build_api_client(client_stub)


def test_login__connection_error():
    http_client_stub = MagicMock()
    http_client_stub.post = MagicMock(side_effect=IslandAPIError)

    api_client = build_api_client(http_client_stub)

    with pytest.raises(IslandAPIError):
        api_client.login(TEST_OTP)


AUTH_TOKEN = "auth_token"
TOKEN_TTL_SEC = 15


def patch_login_with_valid_response(http_client_stub: MagicMock):
    http_client_stub.additional_headers = {}
    http_client_stub.post = MagicMock()
    http_client_stub.post.return_value.json.return_value = {
        "response": {
            "user": {
                ACCESS_TOKEN_KEY_NAME: AUTH_TOKEN,
                TOKEN_TTL_KEY_NAME: TOKEN_TTL_SEC,
            }
        }
    }


def test_login():
    http_client_stub = MagicMock()
    patch_login_with_valid_response(http_client_stub)
    api_client = build_api_client(http_client_stub)

    api_client.login(TEST_OTP)

    assert http_client_stub.additional_headers[HTTPIslandAPIClient.TOKEN_HEADER_KEY] == AUTH_TOKEN


def test_login__bad_response():
    http_client_stub = MagicMock()
    http_client_stub.post = MagicMock()
    http_client_stub.post.return_value.json.return_value = {"abc": 123}
    api_client = build_api_client(http_client_stub)

    with pytest.raises(IslandAPIAuthenticationError):
        api_client.login(TEST_OTP)


def test_login__does_not_overwrite_additional_headers():
    http_client_stub = MagicMock()
    patch_login_with_valid_response(http_client_stub)
    http_client_stub.additional_headers = {"Some-Header": "some value"}
    api_client = build_api_client(http_client_stub)

    api_client.login(TEST_OTP)

    assert http_client_stub.additional_headers == {
        "Some-Header": "some value",
        HTTPIslandAPIClient.TOKEN_HEADER_KEY: AUTH_TOKEN,
    }


def test_refresh_token_before_expiration(freezer):
    refreshed_token = "refreshed_auth_token"
    freezer.move_to(datetime.utcfromtimestamp(0).strftime("%Y-%m-%d %H:%M:%S"))
    http_client_stub = MagicMock()
    patch_login_with_valid_response(http_client_stub)
    api_client = build_api_client(http_client_stub)

    api_client.login(TEST_OTP)
    http_client_stub.post.return_value.json.return_value = {
        "response": {
            "user": {
                ACCESS_TOKEN_KEY_NAME: refreshed_token,
                TOKEN_TTL_KEY_NAME: TOKEN_TTL_SEC,
            }
        }
    }
    http_client_stub.get.return_value.content = b"abc"

    freezer.move_to(datetime.utcfromtimestamp(TOKEN_TTL_SEC / 2).strftime("%Y-%m-%d %H:%M:%S"))
    api_client.get_agent_binary(OperatingSystem.LINUX)
    # assert that the token was not refreshed
    http_client_stub.post.assert_called_once()
    assert http_client_stub.additional_headers[HTTPIslandAPIClient.TOKEN_HEADER_KEY] == AUTH_TOKEN

    freezer.move_to(datetime.utcfromtimestamp(TOKEN_TTL_SEC * 0.99).strftime("%Y-%m-%d %H:%M:%S"))
    api_client.get_agent_binary(OperatingSystem.LINUX)
    http_client_stub.post.assert_called_with("/refresh-authentication-token", {})
    assert (
        http_client_stub.additional_headers[HTTPIslandAPIClient.TOKEN_HEADER_KEY] == refreshed_token
    )


def test_refresh_token_retries_on_429(freezer):
    refreshed_token = "refreshed_auth_token"

    def mock_post_refresh_token(*args, **kwargs):
        mock_post_refresh_token.call_count += 1

        if mock_post_refresh_token.call_count <= 1:
            raise IslandAPIRequestLimitExceededError("Too many requests")

        response = requests.Response()
        response.status_code = HTTPStatus.OK
        response.json = MagicMock()
        response.json.return_value = {
            "response": {
                "user": {
                    ACCESS_TOKEN_KEY_NAME: refreshed_token,
                    TOKEN_TTL_KEY_NAME: TOKEN_TTL_SEC,
                }
            }
        }

        return response

    mock_post_refresh_token.call_count = 0

    freezer.move_to(datetime.utcfromtimestamp(0).strftime("%Y-%m-%d %H:%M:%S"))
    http_client_stub = MagicMock()
    http_client_stub.get.return_value.content = b"abc"
    patch_login_with_valid_response(http_client_stub)
    api_client = build_api_client(http_client_stub)

    api_client.login(TEST_OTP)
    http_client_stub.post.side_effect = mock_post_refresh_token

    freezer.move_to(datetime.utcfromtimestamp(TOKEN_TTL_SEC * 0.99).strftime("%Y-%m-%d %H:%M:%S"))
    api_client.get_agent_binary(OperatingSystem.LINUX)

    http_client_stub.post.assert_called_with("/refresh-authentication-token", {})
    assert (
        http_client_stub.additional_headers[HTTPIslandAPIClient.TOKEN_HEADER_KEY] == refreshed_token
    )


def test_island_api_client__get_agent_binary():
    fake_binary = b"agent-binary"
    os = OperatingSystem.LINUX
    http_client_stub = MagicMock()
    response_stub = MagicMock()
    response_stub.content = fake_binary
    http_client_stub.get.return_value = response_stub
    api_client = build_api_client(http_client_stub)

    assert api_client.get_agent_binary(os) == fake_binary
    assert http_client_stub.get.called_with("/agent-binaries/linux")


def test_island_api_client_send_events__serialization():
    events_to_send = [
        Event1(source=AGENT_ID, timestamp=0, a=1),
        Event2(source=AGENT_ID, timestamp=0, b="hello"),
    ]
    expected_json: List[Dict] = [
        {
            "source": "80988359-a1cd-42a2-9b47-5b94b37cd673",
            "target": None,
            "timestamp": 0.0,
            "tags": [],
            "a": 1,
            "type": "Event1",
        },
        {
            "source": "80988359-a1cd-42a2-9b47-5b94b37cd673",
            "target": None,
            "timestamp": 0.0,
            "tags": [],
            "b": "hello",
            "type": "Event2",
        },
    ]
    client_spy = MagicMock()
    api_client = build_api_client(client_spy)

    api_client.send_events(events=events_to_send)

    assert client_spy.post.call_args[0] == ("/agent-events", expected_json)


def test_island_api_client_send_events__serialization_failed():
    client_spy = MagicMock()
    api_client = build_api_client(client_spy)

    with pytest.raises(IslandAPIRequestError):
        api_client.send_events(events=[Event3(source=AGENT_ID, c=1)])


def test_island_api_client__unhandled_exceptions():
    # Make sure errors not related to response parsing are not handled
    http_client_stub = MagicMock()
    http_client_stub.get = MagicMock(side_effect=OSError)
    api_client = build_api_client(http_client_stub)

    with pytest.raises(OSError):
        api_client.get_agent_signals()


def test_island_api_client_get_otp():
    expected_otp = "secret_otp"
    api_client = _build_client_with_json_response({"otp": expected_otp})

    assert api_client.get_otp() == expected_otp


def test_island_api_client_get_otp__incorrect_response():
    expected_otp = "secret_otp"
    api_client = _build_client_with_json_response({"otpP": expected_otp})

    with pytest.raises(IslandAPIResponseParsingError):
        api_client.get_otp()


def test_island_api_client__handled_exceptions():
    http_client_stub = MagicMock()
    http_client_stub.get = MagicMock(side_effect=json.JSONDecodeError)
    api_client = build_api_client(http_client_stub)

    with pytest.raises(IslandAPIResponseParsingError):
        api_client.get_agent_signals()


def test_island_api_client_get_agent_plugin_manifest():
    expected_agent_plugin_manifest = FAKE_MANIFEST_OBJECT
    client_spy = MagicMock()
    client_spy.get.return_value.json.return_value = FAKE_AGENT_MANIFEST_DICT
    api_client = build_api_client(client_spy)

    actual_agent_plugin_manifest = api_client.get_agent_plugin_manifest(
        AgentPluginType.EXPLOITER, FAKE_NAME
    )

    assert actual_agent_plugin_manifest == expected_agent_plugin_manifest


def test_island_api_client_get_agent_plugin_manifest__bad_json():
    client_spy = MagicMock()
    client_spy.get.return_value.json.return_value = {"bogus": "vogus"}
    api_client = build_api_client(client_spy)

    with pytest.raises(IslandAPIResponseParsingError):
        api_client.get_agent_plugin_manifest(AgentPluginType.EXPLOITER, FAKE_NAME)


@pytest.mark.parametrize("timestamp", [TIMESTAMP, None])
def test_island_api_client_get_agent_signals(timestamp):
    expected_agent_signals = AgentSignals(terminate=timestamp)
    api_client = _build_client_with_json_response({"terminate": timestamp})

    actual_agent_signals = api_client.get_agent_signals()

    assert actual_agent_signals == expected_agent_signals


@pytest.mark.parametrize("timestamp", [TIMESTAMP, None])
def test_island_api_client_get_agent_signals__bad_json(timestamp):
    api_client = _build_client_with_json_response({"terminate": timestamp, "discombobulate": 20})

    with pytest.raises(IslandAPIResponseParsingError):
        api_client.get_agent_signals()


@pytest.mark.parametrize("timestamp,expected", [(1663950115, True), (None, False)])
def test_island_api_client_terminate_signal_is_set(
    timestamp: Optional[int],
    expected: bool,
):
    api_client = _build_client_with_json_response({"terminate": timestamp})
    assert api_client.terminate_signal_is_set() is expected


@pytest.mark.parametrize("timestamp", [TIMESTAMP, None])
def test_island_api_client_terminate_signal_is_set__bad_json(timestamp):
    api_client = _build_client_with_json_response({"terminate": timestamp, "discombobulate": 20})

    with pytest.raises(IslandAPIResponseParsingError):
        api_client.terminate_signal_is_set()


def test_island_api_client_get_agent_configuration_schema():
    expected_agent_configuration_schema = {
        "title": "AgentConfigurationSchema",
        "type": "object",
        "properties": {
            "some_field": {"title": "Some Field", "type": "string"},
            "other_field": {"title": "Other Field", "type": "number"},
        },
        "required": ["some_field", "other_field"],
        "additionalProperties": False,
    }
    api_client = _build_client_with_json_response(AgentConfigurationSchema.schema())

    actual_agent_configuration_schema = api_client.get_agent_configuration_schema()
    assert actual_agent_configuration_schema == expected_agent_configuration_schema


@pytest.mark.parametrize(
    "raised_error", [json.JSONDecodeError, requests.JSONDecodeError, ValueError, TypeError]
)
def test_island_api_client_get_agent_configuration_schema__parsing_error(raised_error):
    client_stub = MagicMock()
    client_stub.get = MagicMock(side_effect=raised_error)
    api_client = build_api_client(client_stub)

    with pytest.raises(IslandAPIResponseParsingError):
        api_client.get_agent_configuration_schema()


@pytest.mark.parametrize(
    "raised_error", [json.JSONDecodeError, requests.JSONDecodeError, ValueError, TypeError]
)
def test_island_api_client_get_config__parsing_error(raised_error):
    client_stub = MagicMock()
    client_stub.get = MagicMock(side_effect=raised_error)
    api_client = build_api_client(client_stub)

    with pytest.raises(IslandAPIResponseParsingError):
        api_client.get_config()


@pytest.mark.parametrize(
    "raised_error", [json.JSONDecodeError, requests.JSONDecodeError, ValueError, TypeError]
)
def test_island_api_client_get_credentials_for_propagation__parsing_error(raised_error):
    client_stub = MagicMock()
    client_stub.get = MagicMock(side_effect=raised_error)
    api_client = build_api_client(client_stub)

    with pytest.raises(IslandAPIResponseParsingError):
        api_client.get_credentials_for_propagation()


def test_island_api_client_get_credentials_for_propagation():
    api_client = _build_client_with_json_response(CREDENTIALS_DICTS)

    expected_credentials = [Credentials(**cred) for cred in CREDENTIALS_DICTS]

    returned_credentials = api_client.get_credentials_for_propagation()

    assert returned_credentials == expected_credentials


def test_island_api_client_get_config():
    agent_config_dict = AgentConfiguration(**AGENT_CONFIGURATION).dict(simplify=True)
    api_client = _build_client_with_json_response(agent_config_dict)

    assert api_client.get_config() == AgentConfiguration(**AGENT_CONFIGURATION)
