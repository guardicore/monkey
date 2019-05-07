"""
Define a Document Schema for the Monkey document.
"""
import mongoengine
from mongoengine import Document, StringField, ListField, BooleanField, EmbeddedDocumentField, DateField, \
    EmbeddedDocument, connect, ReferenceField, DateTimeField

from monkey_island.cc.environment.environment import env

connect(db=env.mongo_db_name, host=env.mongo_db_host, port=env.mongo_db_port)


class Config(EmbeddedDocument):
    """
    No need to define this schema here. It will change often and is already is defined in
    monkey_island.cc.services.config_schema.
    See https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.FieldDoesNotExist
    """
    meta = {'strict': False}
    pass


class Creds(EmbeddedDocument):
    """
    TODO get an example of this data, and make it strict
    """
    meta = {'strict': False}
    pass


class PbaResults(EmbeddedDocument):
    ip = StringField()
    hostname = StringField()
    command = StringField()
    name = StringField()
    result = ListField()


class MonkeyTtl(Document):
    meta = {
        'indexes': [
            {
                'name': 'TTL_index',
                'fields': ['expire_at'],
                'expireAfterSeconds': 0
            }
        ]
    }

    expire_at = DateTimeField()


class Monkey(Document):
    """
    This class has 2 main section:
        *   The schema section defines the DB fields in the document. This is the data of the object.
        *   The logic section defines complex questions we can ask about a single document which are asked multiple
            times, somewhat like an API.
    """
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

    def is_dead(self):
        monkey_is_dead = False
        if self.dead:
            monkey_is_dead = True
        else:
            try:
                if MonkeyTtl.objects(id=self.ttl_ref.id).count() == 0:
                    # No TTLs - monkey has timed out. The monkey is MIA
                    monkey_is_dead = True
            except mongoengine.DoesNotExist:
                # Trying to dereference unknown document
                monkey_is_dead = True
        return monkey_is_dead
