from mongoengine import EmbeddedDocument, StringField, ListField


class PbaResults(EmbeddedDocument):
    ip = StringField()
    hostname = StringField()
    command = StringField()
    name = StringField()
    result = ListField()
