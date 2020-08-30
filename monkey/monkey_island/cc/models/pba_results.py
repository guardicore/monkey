from mongoengine import EmbeddedDocument, ListField, StringField


class PbaResults(EmbeddedDocument):
    ip = StringField()
    hostname = StringField()
    command = StringField()
    name = StringField()
    result = ListField()
