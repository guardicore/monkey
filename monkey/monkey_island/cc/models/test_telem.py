"""
Define a Document Schema for the Monkey document.
"""
from mongoengine import Document, StringField


class TestTelem(Document):
    # SCHEMA
    method = StringField(required=True)
    endpoint = StringField(required=True)
    content = StringField(required=True)

    @staticmethod
    def try_drop_collection():
        try:
            TestTelem.drop_collection()
        except Exception:
            pass
