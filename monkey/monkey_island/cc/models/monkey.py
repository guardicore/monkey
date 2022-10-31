"""
Define a Document Schema for the Monkey document.

"""
import ring
from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    DoesNotExist,
    DynamicField,
    FloatField,
    ListField,
    ReferenceField,
    StringField,
)

from common.network.network_utils import get_my_ip_addresses_legacy
from monkey_island.cc.models.monkey_ttl import MonkeyTtl, create_monkey_ttl_document
from monkey_island.cc.server_utils.consts import DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS


class Monkey(Document):
    """
    This class has 2 main section:
    *   The schema section defines the DB fields in the document. This is the
    data of the object.
    *   The logic section defines complex questions we can ask about a single
    document which are asked multiple times, somewhat like an API.
    """

    # SCHEMA
    guid = StringField(required=True)
    should_stop = BooleanField()
    dead = BooleanField()
    hostname = StringField()
    ip_addresses = ListField(StringField())
    launch_time = FloatField()
    modifytime = DateTimeField()
    # TODO make "parent" an embedded document, so this can be removed and the schema explained (
    #  and validated) verbosely.
    # This is a temporary fix, since mongoengine doesn't allow for lists of strings to be null
    # (even with required=False of null=True).
    # See relevant issue: https://github.com/MongoEngine/mongoengine/issues/1904
    parent = ListField(ListField(DynamicField()))
    ttl_ref = ReferenceField(MonkeyTtl)
    tunnel = ReferenceField("self")

    # This field only exists when the monkey is running on an AWS
    aws_instance_id = StringField(required=False)

    # instance. See https://github.com/guardicore/monkey/issues/426.

    # LOGIC
    @staticmethod
    def get_single_monkey_by_id(db_id):
        try:
            return Monkey.objects.get(id=db_id)
        except DoesNotExist as ex:
            raise MonkeyNotFoundError("info: {0} | id: {1}".format(ex, str(db_id)))

    @staticmethod
    # See https://www.python.org/dev/peps/pep-0484/#forward-references
    def get_single_monkey_by_guid(monkey_guid) -> "Monkey":
        try:
            return Monkey.objects.get(guid=monkey_guid)
        except DoesNotExist as ex:
            raise MonkeyNotFoundError("info: {0} | guid: {1}".format(ex, str(monkey_guid)))

    @staticmethod
    def get_latest_modifytime():
        if Monkey.objects.count() > 0:
            return Monkey.objects.order_by("-modifytime").first().modifytime
        return None

    @ring.lru()
    @staticmethod
    def get_label_by_id(object_id):
        current_monkey = Monkey.get_single_monkey_by_id(object_id)
        label = Monkey.get_hostname_by_id(object_id) + " : " + current_monkey.ip_addresses[0]
        local_ips = map(str, get_my_ip_addresses_legacy())
        if len(set(current_monkey.ip_addresses).intersection(local_ips)) > 0:
            label = "MonkeyIsland - " + label
        return label

    @ring.lru()
    @staticmethod
    def get_hostname_by_id(object_id):
        """
        :param object_id: the object ID of a Monkey in the database.
        :return: The hostname of that machine.
        :note: Use this and not monkey.hostname for performance - this is lru-cached.
        """
        return Monkey.get_single_monkey_by_id(object_id).hostname

    # data has TTL of 1 second. This is useful for rapid calls for report generation.
    @ring.lru(expire=1)
    @staticmethod
    def is_monkey(object_id):
        try:
            _ = Monkey.get_single_monkey_by_id(object_id)
            return True
        except:  # noqa: E722
            return False

    def renew_ttl(self, duration=DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS):
        self.ttl_ref = create_monkey_ttl_document(duration)
        self.save()


class MonkeyNotFoundError(Exception):
    pass
