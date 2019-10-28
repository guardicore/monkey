from monkey_island.cc.environment import Environment


class TestingEnvironment(Environment):
    def __init__(self):
        super(TestingEnvironment, self).__init__()
        self.testing = True

    def get_auth_users(self):
        return []
