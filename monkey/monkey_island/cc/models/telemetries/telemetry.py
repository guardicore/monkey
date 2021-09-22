from __future__ import annotations

from mongoengine import DateTimeField, DictField, Document, EmbeddedDocumentField, StringField

from monkey_island.cc.models import CommandControlChannel
from monkey_island.cc.models.utils import document_encryptor
from monkey_island.cc.models.utils.document_encryptor import FieldNotFoundError, SensitiveField
from monkey_island.cc.models.utils.field_encryptors.mimikatz_results_encryptor import (
    MimikatzResultsEncryptor,
)

sensitive_fields = [
    SensitiveField("data.credentials", MimikatzResultsEncryptor),
    SensitiveField("data.mimikatz", MimikatzResultsEncryptor),
]


class Telemetry(Document):

    data = DictField(required=True)
    timestamp = DateTimeField(required=True)
    monkey_guid = StringField(required=True)
    telem_category = StringField(required=True)
    command_control_channel = EmbeddedDocumentField(CommandControlChannel)

    meta = {"strict": False}

    @staticmethod
    def save_telemetry(telemetry_dict: dict):
        try:
            telemetry_dict = document_encryptor.encrypt(sensitive_fields, telemetry_dict)
        except FieldNotFoundError:
            pass  # Not all telemetries require encryption

        cc_channel = CommandControlChannel(
            src=telemetry_dict["command_control_channel"]["src"],
            dst=telemetry_dict["command_control_channel"]["dst"],
        )
        Telemetry(
            data=telemetry_dict["data"],
            timestamp=telemetry_dict["timestamp"],
            monkey_guid=telemetry_dict["monkey_guid"],
            telem_category=telemetry_dict["telem_category"],
            command_control_channel=cc_channel,
        ).save()

    @staticmethod
    def get_telemetry() -> dict:
        telemetry_dict = Telemetry.objects.first().to_mongo()
        return document_encryptor.decrypt(sensitive_fields, telemetry_dict)
