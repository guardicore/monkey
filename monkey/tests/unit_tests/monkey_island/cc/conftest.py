import monkey_island.cc.environment.environment_singleton as env_singleton
from monkey_island.cc.environment.testing import TestingEnvironment

# Mock environment singleton because it contains mongodb parameters
# needed for model tests. See monkey/monkey_island/cc/models/__init__.py
env_config = {}
env_singleton.env = TestingEnvironment(env_config)

# Without these imports pytests can't use fixtures,
# because they are not found
from tests.unit_tests.monkey_island.cc.mongomock_fixtures import *  # noqa: F401,F403,E402
