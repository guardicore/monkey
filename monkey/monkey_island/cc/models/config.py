from mongoengine import EmbeddedDocument


class Config(EmbeddedDocument):
    """
    No need to define this schema here. It will change often and is already is defined in
    monkey_island.cc.services.config_schema.
    See https://mongoengine-odm.readthedocs.io/apireference.html#mongoengine.FieldDoesNotExist
    """
    meta = {'strict': False}
    pass
