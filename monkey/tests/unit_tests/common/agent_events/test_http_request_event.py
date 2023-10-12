from http import HTTPMethod
from uuid import UUID

import pytest

from common.agent_events import HTTPRequestEvent

AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292
HTTP_URL = "http://www.test.org/RESTFUL/test?filter=my_filter"
HTTPS_URL = "https://www.test.org/RESTFUL/test?filter=my_filter"
METHOD = HTTPMethod.GET


@pytest.mark.parametrize("url", (HTTP_URL, HTTPS_URL))
def test_constructor(url: str):
    event = HTTPRequestEvent(source=AGENT_ID, timestamp=TIMESTAMP, method=METHOD, url=url)

    assert event.source == AGENT_ID
    assert event.timestamp == TIMESTAMP
    assert event.target is None
    assert len(event.tags) == 0
    assert event.method == METHOD
    assert str(event.url) == url


@pytest.mark.parametrize(
    "invalid_url", ("www.missing-schema.org", -1, None, "ftp://wrong.schema.org")
)
def test_invalid_url(invalid_url):
    with pytest.raises((ValueError, TypeError)):
        HTTPRequestEvent(
            source=AGENT_ID,
            timestamp=TIMESTAMP,
            method=METHOD,
            url=invalid_url,
        )


@pytest.mark.parametrize("invalid_method", ("not-a-method", "POST/GET", None, 999))
def test_invalid_method(invalid_method):
    with pytest.raises((ValueError, TypeError)):
        HTTPRequestEvent(source=AGENT_ID, timestamp=TIMESTAMP, method=invalid_method, url=HTTP_URL)
