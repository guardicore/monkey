from monkey_island.cc.environment import Environment, EnvironmentConfig


class TestingEnvironment(Environment):
    """
    Use this environment for running Unit Tests.
    This will cause all mongo connections to happen via `mongomock` instead of using an actual mongodb instance.
    """

    _credentials_required = True

    def __init__(self, config: EnvironmentConfig):
        super(TestingEnvironment, self).__init__(config)
        self.testing = True

    def get_auth_users(self):
        return []
