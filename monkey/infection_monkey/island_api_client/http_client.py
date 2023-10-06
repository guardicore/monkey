import functools
import logging
from enum import Enum, auto
from http import HTTPStatus
from typing import Any, Dict, Optional

import requests
from monkeytypes import JSONSerializable
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT

from .island_api_client_errors import (
    IslandAPIAuthenticationError,
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPIRequestLimitExceededError,
    IslandAPITimeoutError,
)

logger = logging.getLogger(__name__)

# Retries improve reliability and slightly mitigate performance issues
RETRIES = 5


class RequestMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()


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
            _handle_http_error(err)
        except TimeoutError as err:
            raise IslandAPITimeoutError(err)
        except Exception as err:
            raise IslandAPIError(err)

    return decorated


def _handle_http_error(http_error: requests.exceptions.HTTPError):
    if http_error.response.status_code in [
        HTTPStatus.UNAUTHORIZED.value,
        HTTPStatus.FORBIDDEN.value,
    ]:
        raise IslandAPIAuthenticationError(http_error)
    if http_error.response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        raise IslandAPIRequestLimitExceededError(http_error)
    if 400 <= http_error.response.status_code < 500:
        raise IslandAPIRequestError(http_error)
    if 500 <= http_error.response.status_code < 600:
        raise IslandAPIRequestFailedError(http_error)

    raise IslandAPIError(http_error)


class HTTPClient:
    def __init__(self, server_url: str, retries=RETRIES):
        if not server_url.startswith("https://"):
            raise ValueError("Only HTTPS protocol is supported by HTTPClient")
        self._server_url = server_url

        self._session = requests.Session()
        retry_config = Retry(retries)
        self._session.mount("https://", HTTPAdapter(max_retries=retry_config))
        self.additional_headers: Dict[str, Any] = {}

    def get(
        self,
        endpoint: str = "",
        params: Optional[Dict[str, Any]] = None,
        timeout=MEDIUM_REQUEST_TIMEOUT,
        *args,
        **kwargs,
    ) -> requests.Response:
        return self._send_request(
            RequestMethod.GET, endpoint, params=params, timeout=timeout, *args, **kwargs
        )

    def post(
        self,
        endpoint: str = "",
        data: Optional[JSONSerializable] = None,
        timeout=MEDIUM_REQUEST_TIMEOUT,
        *args,
        **kwargs,
    ) -> requests.Response:
        return self._send_request(
            RequestMethod.POST, endpoint, json=data, timeout=timeout, *args, **kwargs
        )

    def put(
        self,
        endpoint: str = "",
        data: Optional[JSONSerializable] = None,
        timeout=MEDIUM_REQUEST_TIMEOUT,
        *args,
        **kwargs,
    ) -> requests.Response:
        return self._send_request(
            RequestMethod.PUT, endpoint, json=data, timeout=timeout, *args, **kwargs
        )

    @handle_island_errors
    def _send_request(
        self,
        request_type: RequestMethod,
        endpoint: str,
        timeout=MEDIUM_REQUEST_TIMEOUT,
        *args,
        **kwargs,
    ) -> requests.Response:
        if self._server_url is None:
            raise RuntimeError("HTTP client does not have a server URL set")
        url = f"{self._server_url.strip('/')}/{endpoint.strip('/')}".strip("/")
        logger.debug(f"{request_type.name} {url}, timeout={timeout}")

        method = getattr(self._session, str.lower(request_type.name))
        response = method(
            url, *args, timeout=timeout, verify=False, headers=self.additional_headers, **kwargs
        )
        response.raise_for_status()

        return response
