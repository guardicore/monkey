from typing import List

from monkey_island.cc.resources.auth.auth_user import User


class UserStore:
    users = []
    username_table = {}

    @staticmethod
    def set_users(users: List[User]):
        UserStore.users = users
        UserStore.username_table = {u.username: u for u in UserStore.users}
