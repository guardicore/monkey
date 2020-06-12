from monkey_island.cc.resources.auth.auth_user import User
from monkey_island.cc.testing.IslandTestCase import IslandTestCase
from monkey_island.cc.environment.aws import AwsEnvironment

import hashlib


class TestAwsEnvironment(IslandTestCase):
    def test_get_auth_users(self):
        env = AwsEnvironment()
        # This is "injecting" the instance id to the env. This is the UTs aren't always executed on the same AWS machine
        # (might not be an AWS machine at all).
        # Perhaps it would have been more elegant to create a Mock, but not worth it for
        # this small test.
        env._instance_id = "i-666"
        hash_obj = hashlib.sha3_512()
        hash_obj.update(b"i-666")
        auth_users = env.get_auth_users()
        assert isinstance(auth_users, list)
        assert len(auth_users) == 1
        auth_user = auth_users[0]
        assert isinstance(auth_user, User)
        assert auth_user.id == 1
        assert auth_user.username == "monkey"
        assert auth_user.secret == hash_obj.hexdigest()
