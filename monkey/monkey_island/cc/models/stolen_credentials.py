from __future__ import annotations

from mongoengine import Document, ListField, ReferenceField

from monkey_island.cc.models import Monkey


class StolenCredentials(Document):
    """
    This class has 2 main section:
    *   The schema section defines the DB fields in the document. This is the
    data of the object.
    *   The logic section defines complex questions we can ask about a single document
    which are asked multiple times, somewhat like an API.

    """

    # SCHEMA
    monkey = ReferenceField(Monkey)
    identities = ListField()
    secrets = ListField()
