from http import HTTPStatus
from typing import Dict

import requests
from monkeytypes import OTP, AgentID

from .i_monkey_island_requests import IMonkeyIslandRequests


class InvalidRequestError(Exception):
    pass


class AgentRequests(IMonkeyIslandRequests):
    def __init__(self, server_address, agent_id: AgentID, otp: OTP):
        self.addr = f"https://{server_address}/"
        self.token = None
        self.agent_id = agent_id
        self.otp = otp

    def login(self):
        self.token = self._try_register_otp()

    def _try_register_otp(self):
        resp = requests.post(  # noqa: DUO123
            self.addr + "api/agent-otp-login",
            json={"agent_id": str(self.agent_id), "otp": self.otp.get_secret_value()},
            verify=False,
        )
        if resp.status_code == HTTPStatus.CONFLICT:
            # A user has already been registered
            return self.get_token_from_server()

        if resp.status_code == HTTPStatus.BAD_REQUEST:
            raise InvalidRequestError()

        token = resp.json()["response"]["user"]["authentication_token"]
        return token

    def get_token_from_server(self):
        return self.token

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

    def put_json(self, url, json: Dict):
        return requests.put(  # noqa: DUO123
            self.addr + url, json=json, headers=self.get_auth_header(), verify=False
        )

    def post_json(self, url, json: Dict):
        return requests.post(  # noqa: DUO123
            self.addr + url, json=json, headers=self.get_auth_header(), verify=False
        )

    def patch(self, url, data: Dict):
        return requests.patch(  # noqa: DUO123
            self.addr + url, data=data, headers=self.get_auth_header(), verify=False
        )

    def delete(self, url):
        return requests.delete(  # noqa: DUO123
            self.addr + url, headers=self.get_auth_header(), verify=False
        )

    def get_auth_header(self):
        return {"Authentication-Token": self.token}
