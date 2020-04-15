"""
Define a Document Schema for the Monkey document.
"""
from mongoengine import Document, StringField


class TestTelem(Document):
    # SCHEMA
    name = StringField(required=True)
    method = StringField(required=True)
    endpoint = StringField(required=True)
    content = StringField(required=True)
