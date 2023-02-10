from unittest.mock import MagicMock

import pytest

from monkey_island.cc.resources.auth import RegistrationStatus

REGISTRATION_STATUS_URL = RegistrationStatus.urls[0]


@pytest.mark.parametrize("needs_registration", [True, False])
def test_needs_registration(flask_client, mock_authentication_service, needs_registration):
    mock_authentication_service.needs_registration = MagicMock(return_value=needs_registration)
    response = flask_client.get(REGISTRATION_STATUS_URL, follow_redirects=True)

    assert response.status_code == 200
    assert response.json["needs_registration"] is needs_registration
