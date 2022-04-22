from mongoengine import BooleanField, EmbeddedDocument


class Config(EmbeddedDocument):

    COLLECTION_NAME = "config"

    """
    No need to define this schema here. It will change often and is already is defined in
    monkey_island.cc.services.config_schema.
    See https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.FieldDoesNotExist
    """

    should_stop = BooleanField()
    meta = {"strict": False}
    pass
