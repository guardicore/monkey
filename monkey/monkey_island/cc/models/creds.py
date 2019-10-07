from mongoengine import EmbeddedDocument


class Creds(EmbeddedDocument):
    """
    TODO get an example of this data, and make it strict
    """
    meta = {'strict': False}
    pass
