from cc.environment import Environment
import cc.auth

__author__ = 'itay.mizeretz'


class PasswordEnvironment(Environment):

    def get_auth_users(self):
        return [
            cc.auth.User(1, self.config['user'], self.config['hash'])
        ]
