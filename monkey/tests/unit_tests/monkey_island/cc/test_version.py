from unittest.mock import MagicMock

import pytest
import requests

from monkey_island.cc import Version
from monkey_island.cc.deployment import Deployment

failed_response = MagicMock()
failed_response.return_value.json.return_value = {"message": "Internal server error"}

successful_response = MagicMock()
SUCCESS_VERSION = "1.1.1"
SUCCESS_URL = "http://be_free.gov"
successful_response.return_value.json.return_value = {
    "version": SUCCESS_VERSION,
    "download_link": SUCCESS_URL,
}


@pytest.mark.parametrize(
    "request_mock",
    [
        failed_response,
        MagicMock(side_effect=requests.exceptions.RequestException("Timeout or something")),
    ],
)
def test_version__request_failed(monkeypatch, request_mock):
    monkeypatch.setattr("requests.get", request_mock)

    version = Version(version_number="1.0.0", deployment=Deployment.DEVELOP)

    assert version.latest_version == "1.0.0"
    assert version.download_url is None


def test_version__request_successful(monkeypatch):
    monkeypatch.setattr("requests.get", successful_response)

    version = Version(version_number="1.0.0", deployment=Deployment.DEVELOP)

    assert version.latest_version == SUCCESS_VERSION
    assert version.download_url == SUCCESS_URL
