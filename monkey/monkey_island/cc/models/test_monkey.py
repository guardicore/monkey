import uuid
from time import sleep

from monkey import Monkey
from monkey_island.cc.models.monkey import MonkeyNotFoundError
from monkey_island.cc.testing.IslandTestCase import IslandTestCase
from monkey_ttl import MonkeyTtl


class TestMonkey(IslandTestCase):
    """
    Make sure to set server environment to `testing` in server.json! Otherwise this will mess up your mongo instance and
    won't work.

    Also, the working directory needs to be the working directory from which you usually run the island so the
    server.json file is found and loaded.
    """

    def test_is_dead(self):
        self.fail_if_not_testing_env()
        self.clean_monkey_db()

        # Arrange
        alive_monkey_ttl = MonkeyTtl.create_ttl_expire_in(30)
        alive_monkey_ttl.save()
        alive_monkey = Monkey(
            guid=str(uuid.uuid4()),
            dead=False,
            ttl_ref=alive_monkey_ttl.id)
        alive_monkey.save()

        # MIA stands for Missing In Action
        mia_monkey_ttl = MonkeyTtl.create_ttl_expire_in(30)
        mia_monkey_ttl.save()
        mia_monkey = Monkey(guid=str(uuid.uuid4()), dead=False, ttl_ref=mia_monkey_ttl)
        mia_monkey.save()
        # Emulate timeout - ttl is manually deleted here, since we're using mongomock and not a real mongo instance.
        sleep(1)
        mia_monkey_ttl.delete()

        dead_monkey = Monkey(guid=str(uuid.uuid4()), dead=True)
        dead_monkey.save()

        # act + assert
        self.assertTrue(dead_monkey.is_dead())
        self.assertTrue(mia_monkey.is_dead())
        self.assertFalse(alive_monkey.is_dead())

    def test_ttl_renewal(self):
        self.fail_if_not_testing_env()
        self.clean_monkey_db()

        # Arrange
        monkey = Monkey(guid=str(uuid.uuid4()))
        monkey.save()
        self.assertIsNone(monkey.ttl_ref)

        # act + assert
        monkey.renew_ttl()
        self.assertIsNotNone(monkey.ttl_ref)

    def test_get_single_monkey_by_id(self):
        self.fail_if_not_testing_env()
        self.clean_monkey_db()

        # Arrange
        a_monkey = Monkey(guid=str(uuid.uuid4()))
        a_monkey.save()

        # Act + assert
        # Find the existing one
        self.assertIsNotNone(Monkey.get_single_monkey_by_id(a_monkey.id))
        # Raise on non-existent monkey
        self.assertRaises(MonkeyNotFoundError, Monkey.get_single_monkey_by_id, "abcdefabcdefabcdefabcdef")

    def test_get_os(self):
        self.fail_if_not_testing_env()
        self.clean_monkey_db()

        linux_monkey = Monkey(guid=str(uuid.uuid4()),
                              description="Linux shay-Virtual-Machine 4.15.0-50-generic #54-Ubuntu SMP Mon May 6 18:46:08 UTC 2019 x86_64 x86_64")
        windows_monkey = Monkey(guid=str(uuid.uuid4()),
                                description="Windows bla bla bla")
        unknown_monkey = Monkey(guid=str(uuid.uuid4()),
                                description="bla bla bla")
        linux_monkey.save()
        windows_monkey.save()
        unknown_monkey.save()

        self.assertEquals(1, len(filter(lambda m: m.get_os() == "windows", Monkey.objects())))
        self.assertEquals(1, len(filter(lambda m: m.get_os() == "linux", Monkey.objects())))
        self.assertEquals(1, len(filter(lambda m: m.get_os() == "unknown", Monkey.objects())))
