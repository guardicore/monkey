from typing import Dict
from unittest import TestCase

from monkey_island.cc.environment import Environment, EnvironmentConfig


class TestEnvironment(TestCase):
    def _test_bool_env_method(
        self, method_name: str, env: Environment, config: Dict, expected_result: bool
    ):
        env._config = EnvironmentConfig(config)
        method = getattr(env, method_name)
        if expected_result:
            self.assertTrue(method())
        else:
            self.assertFalse(method())
