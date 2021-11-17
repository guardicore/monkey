import logging
import uuid

import pytest

from monkey_island.cc.models.monkey import Monkey, MonkeyNotFoundError
from monkey_island.cc.models.monkey_ttl import MonkeyTtl

logger = logging.getLogger(__name__)


class TestMonkey:
    @pytest.mark.usefixtures("uses_database")
    def test_is_dead(self):
        # Arrange
        alive_monkey_ttl = MonkeyTtl.create_ttl_expire_in(30)
        alive_monkey_ttl.save()
        alive_monkey = Monkey(guid=str(uuid.uuid4()), dead=False, ttl_ref=alive_monkey_ttl.id)
        alive_monkey.save()

        # MIA stands for Missing In Action
        mia_monkey_ttl = MonkeyTtl.create_ttl_expire_in(30)
        mia_monkey_ttl.save()
        mia_monkey = Monkey(guid=str(uuid.uuid4()), dead=False, ttl_ref=mia_monkey_ttl.id)
        mia_monkey.save()

        # Emulate timeout - ttl is manually deleted here, since we're using mongomock and not a
        # real mongo instance.
        mia_monkey_ttl.delete()

        dead_monkey = Monkey(guid=str(uuid.uuid4()), dead=True)
        dead_monkey.save()

        # act + assert
        assert dead_monkey.is_dead()
        assert mia_monkey.is_dead()
        assert not alive_monkey.is_dead()

    @pytest.mark.usefixtures("uses_database")
    def test_ttl_renewal(self):
        # Arrange
        monkey = Monkey(guid=str(uuid.uuid4()))
        monkey.save()
        assert monkey.ttl_ref is None

        # act + assert
        monkey.renew_ttl()
        assert monkey.ttl_ref

    @pytest.mark.usefixtures("uses_database")
    def test_get_single_monkey_by_id(self):
        # Arrange
        a_monkey = Monkey(guid=str(uuid.uuid4()))
        a_monkey.save()

        # Act + assert
        # Find the existing one
        assert Monkey.get_single_monkey_by_id(a_monkey.id) is not None

        # Raise on non-existent monkey
        with pytest.raises(MonkeyNotFoundError) as _:
            _ = Monkey.get_single_monkey_by_id("abcdefabcdefabcdefabcdef")

    @pytest.mark.usefixtures("uses_database")
    def test_get_os(self):
        linux_monkey = Monkey(
            guid=str(uuid.uuid4()),
            description="Linux shay-Virtual-Machine 4.15.0-50-generic #54-Ubuntu",
        )
        windows_monkey = Monkey(guid=str(uuid.uuid4()), description="Windows bla bla bla")
        unknown_monkey = Monkey(guid=str(uuid.uuid4()), description="bla bla bla")
        linux_monkey.save()
        windows_monkey.save()
        unknown_monkey.save()

        assert 1 == len([m for m in Monkey.objects() if m.get_os() == "windows"])
        assert 1 == len([m for m in Monkey.objects() if m.get_os() == "linux"])
        assert 1 == len([m for m in Monkey.objects() if m.get_os() == "unknown"])

    @pytest.mark.usefixtures("uses_database")
    def test_get_tunneled_monkeys(self):
        linux_monkey = Monkey(guid=str(uuid.uuid4()), description="Linux shay-Virtual-Machine")
        windows_monkey = Monkey(
            guid=str(uuid.uuid4()), description="Windows bla bla bla", tunnel=linux_monkey
        )
        unknown_monkey = Monkey(
            guid=str(uuid.uuid4()), description="bla bla bla", tunnel=windows_monkey
        )
        linux_monkey.save()
        windows_monkey.save()
        unknown_monkey.save()
        tunneled_monkeys = Monkey.get_tunneled_monkeys()
        test = bool(
            windows_monkey in tunneled_monkeys
            and unknown_monkey in tunneled_monkeys
            and linux_monkey not in tunneled_monkeys
            and len(tunneled_monkeys) == 2
        )
        assert test

    @pytest.mark.usefixtures("uses_database")
    def test_get_label_by_id(self):
        hostname_example = "a_hostname"
        ip_example = "1.1.1.1"
        linux_monkey = Monkey(
            guid=str(uuid.uuid4()),
            description="Linux shay-Virtual-Machine",
            hostname=hostname_example,
            ip_addresses=[ip_example],
        )
        linux_monkey.save()

        logger.debug(id(Monkey.get_label_by_id))

        cache_info_before_query = Monkey.get_label_by_id.storage.backend.cache_info()
        assert cache_info_before_query.hits == 0
        assert cache_info_before_query.misses == 0

        # not cached
        label = Monkey.get_label_by_id(linux_monkey.id)
        cache_info_after_query_1 = Monkey.get_label_by_id.storage.backend.cache_info()
        assert cache_info_after_query_1.hits == 0
        assert cache_info_after_query_1.misses == 1
        logger.debug("1) ID: {} label: {}".format(linux_monkey.id, label))

        assert label is not None
        assert hostname_example in label
        assert ip_example in label

        # should be cached
        label = Monkey.get_label_by_id(linux_monkey.id)
        logger.debug("2) ID: {} label: {}".format(linux_monkey.id, label))
        cache_info_after_query_2 = Monkey.get_label_by_id.storage.backend.cache_info()
        assert cache_info_after_query_2.hits == 1
        assert cache_info_after_query_2.misses == 1

        # should be a another hit, since the monkey ID is already cached
        label = Monkey.get_label_by_id(linux_monkey.id)
        logger.debug("3) ID: {} label: {}".format(linux_monkey.id, label))
        cache_info_after_query_3 = Monkey.get_label_by_id.storage.backend.cache_info()
        logger.debug("Cache info: {}".format(str(cache_info_after_query_3)))
        # still 1 hit only
        assert cache_info_after_query_3.hits == 2
        assert cache_info_after_query_3.misses == 1

    @pytest.mark.usefixtures("uses_database")
    def test_is_monkey(self):
        a_monkey = Monkey(guid=str(uuid.uuid4()))
        a_monkey.save()

        cache_info_before_query = Monkey.is_monkey.storage.backend.cache_info()
        assert cache_info_before_query.hits == 0

        # not cached
        assert Monkey.is_monkey(a_monkey.id)
        fake_id = "123456789012"
        assert not Monkey.is_monkey(fake_id)

        # should be cached
        assert Monkey.is_monkey(a_monkey.id)
        assert not Monkey.is_monkey(fake_id)

        cache_info_after_query = Monkey.is_monkey.storage.backend.cache_info()
        assert cache_info_after_query.hits == 2
