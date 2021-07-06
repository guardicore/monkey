from monkey_island.cc.environment import Environment
from monkey_island.cc.resources.auth.auth_user import User


class StandardEnvironment(Environment):
    _credentials_required = False

    NO_AUTH_USER = "1234567890!@#$%^&*()_nothing_up_my_sleeve_1234567890!@#$%^&*()"
    NO_AUTH_SECRET = "$2b$12$frH7uEwV3jkDNGgReW6j2udw8hy/Yw1SWAqytrcBYK48kn1V5lQIa"

    def get_auth_users(self):
        return [User(1, StandardEnvironment.NO_AUTH_USER, StandardEnvironment.NO_AUTH_SECRET)]
