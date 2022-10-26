from mongoengine import DateTimeField, Document, DynamicField, StringField


class Telemetry(Document):

    data = DynamicField(required=True)
    timestamp = DateTimeField(required=True)
    monkey_guid = StringField(required=True)
    telem_category = StringField(required=True)

    meta = {"strict": False}
