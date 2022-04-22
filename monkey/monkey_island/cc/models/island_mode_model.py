from mongoengine import Document, StringField


class IslandMode(Document):
    COLLECTION_NAME = "island_mode"

    mode = StringField()
