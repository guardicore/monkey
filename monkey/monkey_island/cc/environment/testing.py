from monkey_island.cc.environment import Environment


class TestingEnvironment(Environment):
    """
    Use this environment for running Unit Tests.
    This will cause all mongo connections to happen via `mongomock` instead of using an actual mongodb instance.    
    """
    def __init__(self):
        super(TestingEnvironment, self).__init__()
        self.testing = True

    def get_auth_users(self):
        return []
