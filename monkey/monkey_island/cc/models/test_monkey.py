import uuid
from time import sleep
from unittest import TestCase

from monkey import Monkey
from monkey_island.cc.models.monkey import MonkeyNotFoundError
from monkey_ttl import MonkeyTtl


class TestMonkey(TestCase):
    """
    Make sure to set server environment to `testing` in server.json! Otherwise this will mess up your mongo instance and
    won't work.

    Also, the working directory needs to be the working directory from which you usually run the island so the
    server.json file is found and loaded.
    """
    def test_is_dead(self):
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

    def test_get_single_monkey_by_id(self):
        # Arrange
        a_monkey = Monkey(guid=str(uuid.uuid4()))
        a_monkey.save()

        # Act + assert
        # Find the existing one
        self.assertIsNotNone(Monkey.get_single_monkey_by_id(a_monkey.id))
        # Raise on non-existent monkey
        self.assertRaises(MonkeyNotFoundError, Monkey.get_single_monkey_by_id, "abcdefabcdefabcdefabcdef")
