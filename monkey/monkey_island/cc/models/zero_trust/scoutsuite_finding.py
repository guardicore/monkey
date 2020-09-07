from datetime import datetime

from mongoengine import DateTimeField, EmbeddedDocument, StringField


class ScoutsuiteFinding(EmbeddedDocument):
    # SCHEMA
    temp = StringField(required=True)

    # LOGIC
    @staticmethod
    def create_scoutsuite_finding(title, message, event_type, timestamp=None):
        scoutsuite_finding = ScoutsuiteFinding()

        scoutsuite_finding.temp = "temp"

        return scoutsuite_finding
