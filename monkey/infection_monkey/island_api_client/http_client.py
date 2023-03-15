import functools
import logging
from enum import Enum, auto
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from common.types import JSONSerializable

from .island_api_client_errors import (
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
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


class HTTPClient:
    def __init__(self, retries=RETRIES):
        self._session = requests.Session()
        retry_config = Retry(retries)
        self._session.mount("https://", HTTPAdapter(max_retries=retry_config))
        self._server_url: Optional[str] = None
        self._additional_headers = None

    @property
    def server_url(self):
        return self._server_url

    @server_url.setter
    def server_url(self, endpoint: Optional[str]):
        if endpoint:
            endpoint = f"https://{endpoint}"
        self._server_url = endpoint

    @property
    def additional_headers(self):
        return self._additional_headers

    @additional_headers.setter
    def additional_headers(self, headers: Dict[str, Any]):
        self._additional_headers = headers

    def get(
        self,
        endpoint: str,
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
        endpoint: str,
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
        endpoint: str,
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
        url = f"{self._server_url}{endpoint}".strip("/")
        logger.debug(f"{request_type.name} {url}, timeout={timeout}")

        method = getattr(self._session, str.lower(request_type.name))
        response = method(
            url, *args, timeout=timeout, verify=False, headers=self._additional_headers, **kwargs
        )
        response.raise_for_status()

        return response
