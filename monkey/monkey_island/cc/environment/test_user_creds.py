from unittest import TestCase

from monkey_island.cc.environment.user_creds import UserCreds


class TestUserCreds(TestCase):

    def test_to_dict(self):
        user_creds = UserCreds()
        self.assertDictEqual(user_creds.to_dict(), {})

        user_creds = UserCreds(username="Test")
        self.assertDictEqual(user_creds.to_dict(), {'user': "Test"})

        user_creds = UserCreds(password_hash="abc1231234")
        self.assertDictEqual(user_creds.to_dict(), {'password_hash': "abc1231234"})

        user_creds = UserCreds(username="Test", password_hash="abc1231234")
        self.assertDictEqual(user_creds.to_dict(), {'user': "Test", 'password_hash': "abc1231234"})

    def test_to_auth_user(self):
        user_creds = UserCreds(username="Test", password_hash="abc1231234")
        auth_user = user_creds.to_auth_user()
        self.assertEqual(auth_user.id, 1)
        self.assertEqual(auth_user.username, "Test")
        self.assertEqual(auth_user.secret, "abc1231234")

        user_creds = UserCreds(username="Test")
        auth_user = user_creds.to_auth_user()
        self.assertEqual(auth_user.id, 1)
        self.assertEqual(auth_user.username, "Test")
        self.assertEqual(auth_user.secret, "")

        user_creds = UserCreds(password_hash="abc1231234")
        auth_user = user_creds.to_auth_user()
        self.assertEqual(auth_user.id, 1)
        self.assertEqual(auth_user.username, "")
        self.assertEqual(auth_user.secret, "abc1231234")
