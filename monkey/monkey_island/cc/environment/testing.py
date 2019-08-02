from monkey_island.cc.environment import Environment
import monkey_island.cc.auth


class TestingEnvironment(Environment):
    def __init__(self):
        super(TestingEnvironment, self).__init__()
        self.testing = True

    # SHA3-512 of '1234567890!@#$%^&*()_nothing_up_my_sleeve_1234567890!@#$%^&*()'
    NO_AUTH_CREDS = '55e97c9dcfd22b8079189ddaeea9bce8125887e3237b800c6176c9afa80d2062' \
                    '8d2c8d0b1538d2208c1444ac66535b764a3d902b35e751df3faec1e477ed3557'

    def get_auth_users(self):
        return [
            monkey_island.cc.auth.User(1, self.NO_AUTH_CREDS, self.NO_AUTH_CREDS)
        ]
