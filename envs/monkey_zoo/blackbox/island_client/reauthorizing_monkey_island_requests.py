import functools
from http import HTTPStatus
from typing import Dict

from .i_monkey_island_requests import IMonkeyIslandRequests


class ReauthorizingMonkeyIslandRequests(IMonkeyIslandRequests):
    def __init__(self, monkey_island_requests: IMonkeyIslandRequests):
        self.requests = monkey_island_requests

    def get_token_from_server(self):
        return self.requests.get_token_from_server()

    def login(self):
        self.requests.login()

    class _Decorators:
        @classmethod
        def refresh_auth_token(cls, request_function):
            @functools.wraps(request_function)
            def request_function_wrapper(self, *args, **kwargs):
                # noinspection PyArgumentList
                resp = request_function(self, *args, **kwargs)
                if resp.status_code == HTTPStatus.UNAUTHORIZED:
                    self.requests.login()
                    resp = request_function(self, *args, **kwargs)

                return resp

            return request_function_wrapper

    @_Decorators.refresh_auth_token
    def get(self, url, data=None):
        return self.requests.get(url, data=data)  # noqa: DUO123

    @_Decorators.refresh_auth_token
    def post(self, url, data):
        return self.requests.post(url, data=data)  # noqa: DUO123

    @_Decorators.refresh_auth_token
    def put(self, url, data):
        return self.requests.put(url, data=data)  # noqa: DUO123

    @_Decorators.refresh_auth_token
    def put_json(self, url, json: Dict):
        return self.requests.put_json(url, json=json)  # noqa: DUO123

    @_Decorators.refresh_auth_token
    def post_json(self, url, json: Dict):
        return self.requests.post_json(url, json=json)  # noqa: DUO123

    @_Decorators.refresh_auth_token
    def patch(self, url, data: Dict):
        return self.requests.patch(url, data=data)  # noqa: DUO123

    @_Decorators.refresh_auth_token
    def delete(self, url):
        return self.requests.delete(url)  # noqa: DUO123
