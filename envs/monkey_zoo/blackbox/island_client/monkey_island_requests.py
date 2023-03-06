import functools
import logging
from http import HTTPStatus
from typing import Dict

import requests

ISLAND_USERNAME = "test"
ISLAND_PASSWORD = "testtest"
LOGGER = logging.getLogger(__name__)


class InvalidRequestError(Exception):
    pass


class MonkeyIslandRequests:
    def __init__(self, server_address):
        self.addr = f"https://{server_address}/"
        self.token = self.try_get_token_from_server()

    def try_get_token_from_server(self):
        try:
            return self.try_set_island_to_credentials()
        except InvalidRequestError:
            return self.get_token_from_server()

    def get_token_from_server(self):
        resp = requests.post(  # noqa: DUO123
            self.addr + "api/login?include_auth_token",
            json={"username": ISLAND_USERNAME, "password": ISLAND_PASSWORD},
            verify=False,
        )

        if resp.status_code == 400:
            raise InvalidRequestError()

        token = resp.json()["response"]["user"]["authentication_token"]
        return token

    def try_set_island_to_credentials(self):
        resp = requests.post(  # noqa: DUO123
            self.addr + "api/register?include_auth_token",
            json={"username": ISLAND_USERNAME, "password": ISLAND_PASSWORD},
            verify=False,
        )

        if resp.status_code == 400:
            raise InvalidRequestError()

        token = resp.json()["response"]["user"]["authentication_token"]
        return token

    class _Decorators:
        @classmethod
        def refresh_auth_token(cls, request_function):
            @functools.wraps(request_function)
            def request_function_wrapper(self, *args, **kwargs):
                # noinspection PyArgumentList
                resp = request_function(self, *args, **kwargs)
                if resp.status_code == HTTPStatus.UNAUTHORIZED:
                    self.token = self.get_token_from_server()
                    resp = request_function(self, *args, **kwargs)

                return resp

            return request_function_wrapper

    @_Decorators.refresh_auth_token
    def get(self, url, data=None):
        return requests.get(  # noqa: DUO123
            self.addr + url,
            headers=self.get_auth_header(),
            params=data,
            verify=False,
        )

    @_Decorators.refresh_auth_token
    def post(self, url, data):
        return requests.post(  # noqa: DUO123
            self.addr + url, data=data, headers=self.get_auth_header(), verify=False
        )

    @_Decorators.refresh_auth_token
    def put(self, url, data):
        return requests.put(  # noqa: DUO123
            self.addr + url, data=data, headers=self.get_auth_header(), verify=False
        )

    @_Decorators.refresh_auth_token
    def put_json(self, url, json: Dict):
        return requests.put(  # noqa: DUO123
            self.addr + url, json=json, headers=self.get_auth_header(), verify=False
        )

    @_Decorators.refresh_auth_token
    def post_json(self, url, json: Dict):
        return requests.post(  # noqa: DUO123
            self.addr + url, json=json, headers=self.get_auth_header(), verify=False
        )

    @_Decorators.refresh_auth_token
    def patch(self, url, data: Dict):
        return requests.patch(  # noqa: DUO123
            self.addr + url, data=data, headers=self.get_auth_header(), verify=False
        )

    @_Decorators.refresh_auth_token
    def delete(self, url):
        return requests.delete(  # noqa: DUO123
            self.addr + url, headers=self.get_auth_header(), verify=False
        )

    def get_auth_header(self):
        return {"Authentication-Token": self.token}
