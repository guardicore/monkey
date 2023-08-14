import logging
from http import HTTPStatus

import requests

from common.types import JSONSerializable

from .i_monkey_island_requests import IMonkeyIslandRequests

ISLAND_USERNAME = "test"
ISLAND_PASSWORD = "testtest"
logger = logging.getLogger(__name__)


class InvalidRequestError(Exception):
    pass


class MonkeyIslandRequests(IMonkeyIslandRequests):
    def __init__(self, server_address):
        self.addr = f"https://{server_address}/"
        self.token = None

    def register(self):
        self.token = self._try_get_token_from_server()

    def _try_get_token_from_server(self):
        try:
            return self._try_set_island_to_credentials()
        except InvalidRequestError:
            return self.get_token_from_server()

    def _try_set_island_to_credentials(self):
        resp = requests.post(  # noqa: DUO123
            self.addr + "api/register",
            json={"username": ISLAND_USERNAME, "password": ISLAND_PASSWORD},
            verify=False,
        )

        if resp.status_code == HTTPStatus.CONFLICT:
            # A user has already been registered
            return self.get_token_from_server()

        if resp.status_code == HTTPStatus.BAD_REQUEST:
            raise InvalidRequestError()

        token = resp.json()["response"]["user"]["authentication_token"]
        return token

    def login(self):
        self.token = self.get_token_from_server()

    def get_token_from_server(self):
        resp = requests.post(  # noqa: DUO123
            self.addr + "api/login",
            json={"username": ISLAND_USERNAME, "password": ISLAND_PASSWORD},
            verify=False,
        )

        if resp.status_code == 400:
            raise InvalidRequestError()

        return MonkeyIslandRequests._parse_auth_token_from_response(resp)

    @staticmethod
    def _parse_auth_token_from_response(response: requests.Response):
        return response.json()["response"]["user"]["authentication_token"]

    def refresh_access_token(self):
        response = self.post("api/refresh-authentication-token", None)
        response.raise_for_status()

        self.token = MonkeyIslandRequests._parse_auth_token_from_response(response)

    def get(self, url, data=None):
        return requests.get(  # noqa: DUO123
            self.addr + url,
            headers=self.get_auth_header(),
            params=data,
            verify=False,
        )

    def post(self, url, data):
        return requests.post(  # noqa: DUO123
            self.addr + url, data=data, headers=self.get_auth_header(), verify=False
        )

    def put(self, url, data):
        return requests.put(  # noqa: DUO123
            self.addr + url, data=data, headers=self.get_auth_header(), verify=False
        )

    def put_json(self, url, json: JSONSerializable):
        return requests.put(  # noqa: DUO123
            self.addr + url, json=json, headers=self.get_auth_header(), verify=False
        )

    def post_json(self, url, json: JSONSerializable):
        return requests.post(  # noqa: DUO123
            self.addr + url, json=json, headers=self.get_auth_header(), verify=False
        )

    def patch(self, url, data: JSONSerializable):
        return requests.patch(  # noqa: DUO123
            self.addr + url, data=data, headers=self.get_auth_header(), verify=False
        )

    def delete(self, url):
        return requests.delete(  # noqa: DUO123
            self.addr + url, headers=self.get_auth_header(), verify=False
        )

    def get_auth_header(self):
        return {"Authentication-Token": self.token}
