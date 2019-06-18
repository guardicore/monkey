"""
Define a Document Schema for the Monkey document.
"""
import mongoengine
from mongoengine import Document, StringField, ListField, BooleanField, EmbeddedDocumentField, DateField, \
    ReferenceField

from monkey_island.cc.models.monkey_ttl import MonkeyTtl


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
    keepalive = DateField()
    modifytime = DateField()
    # TODO change this to an embedded document as well - RN it's an unnamed tuple which is confusing.
    parent = ListField(ListField(StringField()))
    config_error = BooleanField()
    critical_services = ListField(StringField())
    pba_results = ListField()
    ttl_ref = ReferenceField(MonkeyTtl)

    # LOGIC
    @staticmethod
    def get_single_monkey_by_id(db_id):
        try:
            return Monkey.objects(id=db_id)[0]
        except IndexError:
            raise MonkeyNotFoundError("id: {0}".format(str(db_id)))

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


class MonkeyNotFoundError(Exception):
    pass
