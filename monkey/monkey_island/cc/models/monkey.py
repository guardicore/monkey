"""
Define a Document Schema for the Monkey document.
"""
import mongoengine
import logging
from mongoengine import Document, StringField, ListField, BooleanField, EmbeddedDocumentField, ReferenceField, \
    DateTimeField

from monkey_island.cc.models.monkey_ttl import MonkeyTtl, create_monkey_ttl_document
from monkey_island.cc.consts import DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS


logger = logging.getLogger(__name__)

class Monkey(Document):
    """
    This class has 2 main section:
        *   The schema section defines the DB fields in the document. This is the data of the object.
        *   The logic section defines complex questions we can ask about a single document which are asked multiple
            times, somewhat like an API.
    """
    # SCHEMA
    guid = StringField(required=True)
    config = EmbeddedDocumentField('Config')
    creds = ListField(EmbeddedDocumentField('Creds'))
    dead = BooleanField()
    description = StringField()
    hostname = StringField()
    internet_access = BooleanField()
    ip_addresses = ListField(StringField())
    keepalive = DateTimeField()
    modifytime = DateTimeField()
    # TODO change this to an embedded document as well - RN it's an unnamed tuple which is confusing.
    parent = ListField(ListField(StringField()))
    config_error = BooleanField()
    critical_services = ListField(StringField())
    pba_results = ListField()
    ttl_ref = ReferenceField(MonkeyTtl)
    tunnel = ReferenceField("self")

    # LOGIC
    @staticmethod
    def get_single_monkey_by_id(db_id):
        try:
            return Monkey.objects.get(id=db_id)
        except mongoengine.DoesNotExist as ex:
            raise MonkeyNotFoundError("info: {0} | id: {1}".format(ex.message, str(db_id)))

    @staticmethod
    def get_single_monkey_by_guid(monkey_guid):
        try:
            return Monkey.objects.get(guid=monkey_guid)
        except mongoengine.DoesNotExist as ex:
            raise MonkeyNotFoundError("info: {0} | guid: {1}".format(ex.message, str(monkey_guid)))

    @staticmethod
    def get_latest_modifytime():
        if Monkey.objects.count() > 0:
            return Monkey.objects.order_by('-modifytime').first().modifytime
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
            except (mongoengine.DoesNotExist, AttributeError):
                # Trying to dereference unknown document - the monkey is MIA.
                monkey_is_dead = True
        return monkey_is_dead

    def get_os(self):
        os = "unknown"
        if self.description.lower().find("linux") != -1:
            os = "linux"
        elif self.description.lower().find("windows") != -1:
            os = "windows"
        return os

    def renew_ttl(self, duration=DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS):
        self.ttl_ref = create_monkey_ttl_document(duration)


class MonkeyNotFoundError(Exception):
    pass
