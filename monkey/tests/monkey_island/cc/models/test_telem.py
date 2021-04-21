"""
Define a Document Schema for the TestTelem document.
"""
from mongoengine import DateTimeField, Document, StringField


class TestTelem(Document):
    # SCHEMA
    name = StringField(required=True)
    time = DateTimeField(required=True)
    method = StringField(required=True)
    endpoint = StringField(required=True)
    content = StringField(required=True)
