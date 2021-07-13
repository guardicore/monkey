from mongoengine import Document, StringField


class IslandMode(Document):
    mode = StringField()
