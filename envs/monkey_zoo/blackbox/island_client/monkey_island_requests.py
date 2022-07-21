import functools
import logging
from typing import Dict

import requests

ISLAND_USERNAME = "test"
ISLAND_PASSWORD = "test"
LOGGER = logging.getLogger(__name__)


class AuthenticationFailedError(Exception):
    pass


class InvalidRegistrationCredentialsError(Exception):
    pass


# noinspection PyArgumentList
class MonkeyIslandRequests(object):
    def __init__(self, server_address):
        self.addr = "https://{IP}/".format(IP=server_address)
        self.token = self.try_get_jwt_from_server()

    def try_get_jwt_from_server(self):
        try:
            return self.get_jwt_from_server()
        except AuthenticationFailedError:
            self.try_set_island_to_credentials()
            return self.get_jwt_from_server()
        except (requests.ConnectionError, InvalidRegistrationCredentialsError) as err:
            LOGGER.error(
                "Unable to connect to island, aborting! Error information: {}. Server: {}".format(
                    err, self.addr
                )
            )
            assert False

    def get_jwt_from_server(self):
        resp = requests.post(  # noqa: DUO123
            self.addr + "api/auth",
            json={"username": ISLAND_USERNAME, "password": ISLAND_PASSWORD},
            verify=False,
        )
        if resp.status_code == 401:
            raise AuthenticationFailedError
        return resp.json()["access_token"]

    def try_set_island_to_credentials(self):
        resp = requests.post(  # noqa: DUO123
            self.addr + "api/registration",
            json={"username": ISLAND_USERNAME, "password": ISLAND_PASSWORD},
            verify=False,
        )
        if resp.status_code == 400:
            raise InvalidRegistrationCredentialsError("Missing part of the credentials")

    class _Decorators:
        @classmethod
        def refresh_jwt_token(cls, request_function):
            @functools.wraps(request_function)
            def request_function_wrapper(self, *args, **kwargs):
                self.token = self.try_get_jwt_from_server()
                # noinspection PyArgumentList
                return request_function(self, *args, **kwargs)

            return request_function_wrapper

    @_Decorators.refresh_jwt_token
    def get(self, url, data=None):
        return requests.get(  # noqa: DUO123
            self.addr + url,
            headers=self.get_jwt_header(),
            params=data,
            verify=False,
        )

    @_Decorators.refresh_jwt_token
    def post(self, url, data):
        return requests.post(  # noqa: DUO123
            self.addr + url, data=data, headers=self.get_jwt_header(), verify=False
        )

    @_Decorators.refresh_jwt_token
    def post_json(self, url, data: Dict):
        return requests.post(  # noqa: DUO123
            self.addr + url, json=data, headers=self.get_jwt_header(), verify=False
        )

    @_Decorators.refresh_jwt_token
    def patch(self, url, data: Dict):
        return requests.patch(  # noqa: DUO123
            self.addr + url, data=data, headers=self.get_jwt_header(), verify=False
        )

    @_Decorators.refresh_jwt_token
    def delete(self, url):
        return requests.delete(  # noqa: DUO123
            self.addr + url, headers=self.get_jwt_header(), verify=False
        )

    def get_jwt_header(self):
        return {"Authorization": "Bearer " + self.token}
