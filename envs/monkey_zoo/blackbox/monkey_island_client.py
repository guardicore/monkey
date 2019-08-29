import requests

# SHA3-512 of '1234567890!@#$%^&*()_nothing_up_my_sleeve_1234567890!@#$%^&*()'
NO_AUTH_CREDS = '55e97c9dcfd22b8079189ddaeea9bce8125887e3237b800c6176c9afa80d2062' \
                '8d2c8d0b1538d2208c1444ac66535b764a3d902b35e751df3faec1e477ed3557'


class MonkeyIslandClient(object):
    def __init__(self, server_address):
        self.addr = "https://{IP}/".format(IP=server_address)
        self.token = self.get_jwt_token_from_server()

    def get_jwt_token_from_server(self):
        resp = requests.post(self.addr + "api/auth", json={"username": NO_AUTH_CREDS, "password": NO_AUTH_CREDS},
                             verify=False)
        return resp.json()["access_token"]

    def get_api_status(self):
        return requests.get(self.addr + "api", headers={"Authorization": "JWT " + self.token}, verify=False)

    def import_config(self, config_contents):
        resp = requests.post(
            self.addr + "api/configuration/island",
            headers={"Authorization": "JWT " + self.token},
            data=config_contents,
            verify=False)
        print(resp.text)
