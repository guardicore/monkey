from monkey_island.cc.environment import Environment
import monkey_island.cc.auth

__author__ = 'itay.mizeretz'


class PasswordEnvironment(Environment):

    _credentials_required = True

    def get_auth_users(self):
        if 'user' in self.config and 'hash' in self.config:
            return [monkey_island.cc.auth.User(1, self.config['user'], self.config['hash'])]
        else:
            return []
