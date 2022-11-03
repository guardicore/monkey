"""
Define a Document Schema for the Monkey document.

"""
from mongoengine import (
    DateTimeField,
    Document,
    DynamicField,
    FloatField,
    ListField,
    ReferenceField,
    StringField,
)


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
    modifytime = DateTimeField()
    # TODO make "parent" an embedded document, so this can be removed and the schema explained (
    #  and validated) verbosely.
    # This is a temporary fix, since mongoengine doesn't allow for lists of strings to be null
    # (even with required=False of null=True).
    # See relevant issue: https://github.com/MongoEngine/mongoengine/issues/1904
    parent = ListField(ListField(DynamicField()))
    tunnel = ReferenceField("self")

    # This field only exists when the monkey is running on an AWS
    aws_instance_id = StringField(required=False)

    # instance. See https://github.com/guardicore/monkey/issues/426.

    @staticmethod
    def get_latest_modifytime():
        if Monkey.objects.count() > 0:
            return Monkey.objects.order_by("-modifytime").first().modifytime
        return None
