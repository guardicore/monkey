import bcrypt

from monkey_island.cc.environment import Environment
from monkey_island.cc.resources.auth.auth_user import User

__author__ = "itay.mizeretz"


class StandardEnvironment(Environment):
    _credentials_required = False

    NO_AUTH_USER = "1234567890!@#$%^&*()_nothing_up_my_sleeve_1234567890!@#$%^&*()"
    NO_AUTH_SECRET = bcrypt.hashpw(
        NO_AUTH_USER.encode("utf-8"), b"$2b$12$frH7uEwV3jkDNGgReW6j2u"
    ).decode()

    def get_auth_users(self):
        return [User(1, StandardEnvironment.NO_AUTH_USER, StandardEnvironment.NO_AUTH_SECRET)]
