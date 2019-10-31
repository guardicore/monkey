from mongoengine import EmbeddedDocument, StringField


class CommandControlChannel(EmbeddedDocument):
    """
    This value describes command and control channel monkey used in communication
    src - Monkey Island's IP
    dst - Monkey's IP (in case of a proxy chain this is the IP of the last monkey)
    """
    src = StringField()
    dst = StringField()
