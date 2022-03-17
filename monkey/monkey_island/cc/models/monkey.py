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
    EmbeddedDocumentField,
    FloatField,
    ListField,
    ReferenceField,
    StringField,
)

from monkey_island.cc.models.command_control_channel import CommandControlChannel
from monkey_island.cc.models.monkey_ttl import MonkeyTtl, create_monkey_ttl_document
from monkey_island.cc.server_utils.consts import DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS
from monkey_island.cc.services.utils.network_utils import local_ip_addresses


class ParentNotFoundError(Exception):
    """Raise when trying to get a parent of monkey that doesn't have one"""


class Monkey(Document):
    """
    This class has 2 main section:
        *   The schema section defines the DB fields in the document. This is the data of the
        object.
        *   The logic section defines complex questions we can ask about a single document which
        are asked multiple
            times, somewhat like an API.
    """

    # SCHEMA
    guid = StringField(required=True)
    config = EmbeddedDocumentField("Config")
    dead = BooleanField()
    description = StringField()
    hostname = StringField()
    ip_addresses = ListField(StringField())
    networks = ListField()
    launch_time = FloatField()
    modifytime = DateTimeField()
    # TODO make "parent" an embedded document, so this can be removed and the schema explained (
    #  and validated) verbosely.
    # This is a temporary fix, since mongoengine doesn't allow for lists of strings to be null
    # (even with required=False of null=True).
    # See relevant issue: https://github.com/MongoEngine/mongoengine/issues/1904
    parent = ListField(ListField(DynamicField()))
    config_error = BooleanField()
    critical_services = ListField(StringField())
    pba_results = ListField()
    ttl_ref = ReferenceField(MonkeyTtl)
    tunnel = ReferenceField("self")
    command_control_channel = EmbeddedDocumentField(CommandControlChannel)

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

    def is_dead(self):
        monkey_is_dead = False
        if self.dead:
            monkey_is_dead = True
        else:
            try:
                if MonkeyTtl.objects(id=self.ttl_ref.id).count() == 0:
                    # No TTLs - monkey has timed out. The monkey is MIA.
                    monkey_is_dead = True
            except (DoesNotExist, AttributeError):
                # Trying to dereference unknown document - the monkey is MIA.
                monkey_is_dead = True
        return monkey_is_dead

    def has_parent(self):
        for p in self.parent:
            if p[0] != self.guid:
                return True
        return False

    def get_parent(self):
        if self.has_parent():
            return Monkey.objects(guid=self.parent[0][0]).first()
        else:
            raise ParentNotFoundError(f"No parent was found for agent with GUID {self.guid}")

    def get_os(self):
        os = "unknown"
        if self.description.lower().find("linux") != -1:
            os = "linux"
        elif self.description.lower().find("windows") != -1:
            os = "windows"
        return os

    @ring.lru()
    @staticmethod
    def get_label_by_id(object_id):
        current_monkey = Monkey.get_single_monkey_by_id(object_id)
        label = Monkey.get_hostname_by_id(object_id) + " : " + current_monkey.ip_addresses[0]
        if len(set(current_monkey.ip_addresses).intersection(local_ip_addresses())) > 0:
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

    def get_network_info(self):
        """
        Formats network info from monkey's model
        :return: dictionary with an array of IP's and a hostname
        """
        return {"ips": self.ip_addresses, "hostname": self.hostname}

    # data has TTL of 1 second. This is useful for rapid calls for report generation.
    @ring.lru(expire=1)
    @staticmethod
    def is_monkey(object_id):
        try:
            _ = Monkey.get_single_monkey_by_id(object_id)
            return True
        except:  # noqa: E722
            return False

    @staticmethod
    def get_tunneled_monkeys():
        return Monkey.objects(tunnel__exists=True)

    def renew_ttl(self, duration=DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS):
        self.ttl_ref = create_monkey_ttl_document(duration)
        self.save()


class MonkeyNotFoundError(Exception):
    pass
