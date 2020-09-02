import functools
import logging
from datetime import timedelta
from typing import Dict

import requests

from envs.monkey_zoo.blackbox.island_client.supported_request_method import \
    SupportedRequestMethod

# SHA3-512 of '1234567890!@#$%^&*()_nothing_up_my_sleeve_1234567890!@#$%^&*()'
NO_AUTH_CREDS = '55e97c9dcfd22b8079189ddaeea9bce8125887e3237b800c6176c9afa80d2062' \
                '8d2c8d0b1538d2208c1444ac66535b764a3d902b35e751df3faec1e477ed3557'
LOGGER = logging.getLogger(__name__)


# noinspection PyArgumentList
class MonkeyIslandRequests(object):
    def __init__(self, server_address):
        self.addr = "https://{IP}/".format(IP=server_address)
        self.token = self.try_get_jwt_from_server()
        self.supported_request_methods = {SupportedRequestMethod.GET: self.get,
                                          SupportedRequestMethod.POST: self.post,
                                          SupportedRequestMethod.PATCH: self.patch,
                                          SupportedRequestMethod.DELETE: self.delete}

    def get_request_time(self, url, method: SupportedRequestMethod, data=None):
        response = self.send_request_by_method(url, method, data)
        if response.ok:
            LOGGER.debug(f"Got ok for {url} content peek:\n{response.content[:120].strip()}")
            return response.elapsed
        else:
            LOGGER.error(f"Trying to get {url} but got unexpected {str(response)}")
            # instead of raising for status, mark failed responses as maxtime
            return timedelta.max

    def send_request_by_method(self, url, method=SupportedRequestMethod.GET, data=None):
        if data:
            return self.supported_request_methods[method](url, data)
        else:
            return self.supported_request_methods[method](url)

    def try_get_jwt_from_server(self):
        try:
            return self.get_jwt_from_server()
        except requests.ConnectionError as err:
            LOGGER.error(
                "Unable to connect to island, aborting! Error information: {}. Server: {}".format(err, self.addr))
            assert False

    class _Decorators:
        @classmethod
        def refresh_jwt_token(cls, request_function):
            @functools.wraps(request_function)
            def request_function_wrapper(self, *args, **kwargs):
                self.token = self.try_get_jwt_from_server()
                # noinspection PyArgumentList
                return request_function(self, *args, **kwargs)

            return request_function_wrapper

    def get_jwt_from_server(self):
        resp = requests.post(self.addr + "api/auth",  # noqa: DUO123
                             json={"username": NO_AUTH_CREDS, "password": NO_AUTH_CREDS},
                             verify=False)
        return resp.json()["access_token"]

    @_Decorators.refresh_jwt_token
    def get(self, url, data=None):
        return requests.get(self.addr + url,  # noqa: DUO123
                            headers=self.get_jwt_header(),
                            params=data,
                            verify=False)

    @_Decorators.refresh_jwt_token
    def post(self, url, data):
        return requests.post(self.addr + url,  # noqa: DUO123
                             data=data,
                             headers=self.get_jwt_header(),
                             verify=False)

    @_Decorators.refresh_jwt_token
    def post_json(self, url, data: Dict):
        return requests.post(self.addr + url,  # noqa: DUO123
                             json=data,
                             headers=self.get_jwt_header(),
                             verify=False)

    @_Decorators.refresh_jwt_token
    def patch(self, url, data: Dict):
        return requests.patch(self.addr + url,  # noqa: DUO123
                              data=data,
                              headers=self.get_jwt_header(),
                              verify=False)

    @_Decorators.refresh_jwt_token
    def delete(self, url):
        return requests.delete(  # noqa: DOU123
            self.addr + url,
            headers=self.get_jwt_header(),
            verify=False)

    @_Decorators.refresh_jwt_token
    def get_jwt_header(self):
        return {"Authorization": "Bearer " + self.token}
