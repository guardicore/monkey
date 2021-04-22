"""
Define a Document Schema for the TelemForExport document.
"""
from mongoengine import DateTimeField, Document, StringField


# This document describes exported telemetry.
# These telemetries are used to mock monkeys sending telemetries to the island.
# This way we can replicate island state without running monkeys.
class ExportedTelem(Document):
    # SCHEMA
    name = StringField(required=True)
    time = DateTimeField(required=True)
    method = StringField(required=True)
    endpoint = StringField(required=True)
    content = StringField(required=True)
