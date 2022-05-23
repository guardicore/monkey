import json
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer

from monkey_island.cc.resources import RemoteRun
from monkey_island.cc.services import AWSService
from monkey_island.cc.services.aws import AWSCommandResults, AWSCommandStatus


@pytest.fixture
def mock_aws_service():
    return MagicMock(spec=AWSService)


@pytest.fixture
def flask_client(build_flask_client, mock_aws_service):
    container = StubDIContainer()
    container.register_instance(AWSService, mock_aws_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_get_invalid_action(flask_client):
    response = flask_client.get(f"{RemoteRun.urls[0]}?action=INVALID")
    assert response.text.rstrip() == "{}"


def test_get_no_action(flask_client):
    response = flask_client.get(RemoteRun.urls[0])
    assert response.text.rstrip() == "{}"


def test_get_not_aws(flask_client, mock_aws_service):
    mock_aws_service.island_is_running_on_aws = MagicMock(return_value=False)
    response = flask_client.get(f"{RemoteRun.urls[0]}?action=list_aws")
    assert response.text.rstrip() == '{"is_aws":false}'


def test_get_instances(flask_client, mock_aws_service):
    instances = [
        {"instance_id": "1", "name": "name1", "os": "linux", "ip_address": "1.1.1.1"},
        {"instance_id": "2", "name": "name2", "os": "windows", "ip_address": "2.2.2.2"},
        {"instance_id": "3", "name": "name3", "os": "linux", "ip_address": "3.3.3.3"},
    ]
    mock_aws_service.island_is_running_on_aws = MagicMock(return_value=True)
    mock_aws_service.get_managed_instances = MagicMock(return_value=instances)

    response = flask_client.get(f"{RemoteRun.urls[0]}?action=list_aws")

    assert json.loads(response.text)["instances"] == instances
    assert json.loads(response.text)["is_aws"] is True


# TODO: Test error cases for get()


def test_post_no_type(flask_client):
    response = flask_client.post(RemoteRun.urls[0], data="{}")
    assert response.status_code == 500


def test_post_invalid_type(flask_client):
    response = flask_client.post(RemoteRun.urls[0], data='{"type": "INVALID"}')
    assert response.status_code == 500


def test_post(flask_client, mock_aws_service):
    request_body = json.dumps(
        {
            "type": "aws",
            "instances": [
                {"instance_id": "1", "os": "linux"},
                {"instance_id": "2", "os": "linux"},
                {"instance_id": "3", "os": "windows"},
            ],
            "island_ip": "127.0.0.1",
        }
    )
    mock_aws_service.run_agents_on_managed_instances = MagicMock(
        return_value=[
            AWSCommandResults("1", 0, "", "", AWSCommandStatus.SUCCESS),
            AWSCommandResults("2", 0, "some_output", "", AWSCommandStatus.IN_PROGRESS),
            AWSCommandResults("3", -1, "", "some_error", AWSCommandStatus.ERROR),
        ]
    )
    expected_result = [
        {"instance_id": "1", "response_code": 0, "stdout": "", "stderr": "", "status": "success"},
        {
            "instance_id": "2",
            "response_code": 0,
            "stdout": "some_output",
            "stderr": "",
            "status": "in_progress",
        },
        {
            "instance_id": "3",
            "response_code": -1,
            "stdout": "",
            "stderr": "some_error",
            "status": "error",
        },
    ]

    response = flask_client.post(RemoteRun.urls[0], data=request_body)

    assert json.loads(response.text)["result"] == expected_result
