import uuid
from datetime import timedelta, datetime
from time import sleep
from unittest import TestCase

# noinspection PyUnresolvedReferences
import mongomock

from monkey import Monkey
from monkey_island.cc.models.errors import MonkeyNotFoundError
from monkey_ttl import MonkeyTtl


class TestMonkey(TestCase):
    def test_is_dead(self):
        alive_monkey_ttl = MonkeyTtl(expire_at=datetime.now() + timedelta(seconds=30))
        alive_monkey_ttl.save()
        alive_monkey = Monkey(
            guid=str(uuid.uuid4()),
            dead=False,
            ttl_ref=alive_monkey_ttl.id)
        alive_monkey.save()

        mia_monkey_ttl = MonkeyTtl(expire_at=datetime.now() + timedelta(seconds=30))
        mia_monkey_ttl.save()
        mia_monkey = Monkey(guid=str(uuid.uuid4()), dead=False, ttl_ref=mia_monkey_ttl)
        mia_monkey.save()
        # Emulate timeout
        sleep(1)
        mia_monkey_ttl.delete()

        dead_monkey = Monkey(guid=str(uuid.uuid4()), dead=True)
        dead_monkey.save()

        self.assertTrue(dead_monkey.is_dead())
        self.assertTrue(mia_monkey.is_dead())
        self.assertFalse(alive_monkey.is_dead())

    def test_get_single_monkey_by_id(self):
        a_monkey = Monkey(guid=str(uuid.uuid4()))
        a_monkey.save()

        self.assertIsNotNone(Monkey.get_single_monkey_by_id(a_monkey.id))
        self.assertRaises(MonkeyNotFoundError, Monkey.get_single_monkey_by_id, "abcdefabcdefabcdefabcdef")
