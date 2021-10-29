from mongoengine import DateTimeField, Document, DynamicField, EmbeddedDocumentField, StringField

from monkey_island.cc.models import CommandControlChannel


class Telemetry(Document):

    data = DynamicField(required=True)
    timestamp = DateTimeField(required=True)
    monkey_guid = StringField(required=True)
    telem_category = StringField(required=True)
    command_control_channel = EmbeddedDocumentField(CommandControlChannel)

    meta = {"strict": False}
