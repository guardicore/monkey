import json

import requests

# SHA3-512 of '1234567890!@#$%^&*()_nothing_up_my_sleeve_1234567890!@#$%^&*()'
NO_AUTH_CREDS = '55e97c9dcfd22b8079189ddaeea9bce8125887e3237b800c6176c9afa80d2062' \
                '8d2c8d0b1538d2208c1444ac66535b764a3d902b35e751df3faec1e477ed3557'


class MonkeyIslandClient(object):
    def __init__(self, server_address):
        self.addr = "https://{IP}/".format(IP=server_address)
        self.token = self.get_jwt_from_server()

    def get_jwt_from_server(self):
        resp = requests.post(self.addr + "api/auth",
                             json={"username": NO_AUTH_CREDS, "password": NO_AUTH_CREDS},
                             verify=False)
        return resp.json()["access_token"]

    def request_get(self, url, data=None):
        return requests.get(self.addr + url,
                            headers={"Authorization": "JWT " + self.token},
                            params=data,
                            verify=False)

    def request_post(self, url, data):
        return requests.post(self.addr + url,
                             data=data,
                             headers={"Authorization": "JWT " + self.token},
                             verify=False)

    def request_post_json(self, url, dict_data):
        return requests.post(self.addr + url,
                             json=dict_data,
                             headers={"Authorization": "JWT " + self.token},
                             verify=False)

    def get_api_status(self):
        return self.request_get("api")

    def import_config(self, config_contents):
        _ = self.request_post("api/configuration/island", data=config_contents)

    def run_monkey_local(self):
        if self.request_post_json("api/local-monkey", dict_data={"action": "run"}).ok:
            print("Running the monkey.")
        else:
            print("Failed to run the monkey.")
            assert False

    def reset_env(self):
        if self.request_get("api", {"action": "reset"}).ok:
            print("Resetting environment after the test.")
        else:
            print("Failed to reset the environment.")
            assert False
