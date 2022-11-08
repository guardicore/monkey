"""
Define a Document Schema for the Monkey document.

"""
from mongoengine import Document, DynamicField, FloatField, ListField, StringField


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
    hostname = StringField()
    ip_addresses = ListField(StringField())
    launch_time = FloatField()
    # TODO make "parent" an embedded document, so this can be removed and the schema explained (
    #  and validated) verbosely.
    # This is a temporary fix, since mongoengine doesn't allow for lists of strings to be null
    # (even with required=False of null=True).
    # See relevant issue: https://github.com/MongoEngine/mongoengine/issues/1904
    parent = ListField(ListField(DynamicField()))
