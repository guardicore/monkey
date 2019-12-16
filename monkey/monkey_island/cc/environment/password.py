from monkey_island.cc.environment import Environment
import monkey_island.cc.auth

__author__ = 'itay.mizeretz'


class PasswordEnvironment(Environment):

    def get_auth_users(self):
        return [
            monkey_island.cc.auth.User(1, self.config['user'], self.config['hash'])
        ]
