from mongoengine import EmbeddedDocument, StringField


class C2Info(EmbeddedDocument):
    src = StringField()
    dst = StringField()
