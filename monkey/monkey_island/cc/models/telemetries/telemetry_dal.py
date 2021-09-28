from __future__ import annotations

from typing import List

from monkey_island.cc.database import mongo
from monkey_island.cc.models import CommandControlChannel
from monkey_island.cc.models.telemetries.telemetry import Telemetry
from monkey_island.cc.server_utils.encryption import (
    FieldNotFoundError,
    MimikatzResultsEncryptor,
    SensitiveField,
    decrypt_dict,
    encrypt_dict,
)

sensitive_fields = [
    SensitiveField("data.credentials", MimikatzResultsEncryptor),
    SensitiveField("data.mimikatz", MimikatzResultsEncryptor),
]


def save_telemetry(telemetry_dict: dict):
    try:
        telemetry_dict = encrypt_dict(sensitive_fields, telemetry_dict)
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


# A lot of codebase is using queries for telemetry collection and document field encryption is
# not yet implemented in mongoengine. To avoid big time investment, queries are used for now.
def get_telemetry_by_query(query: dict, output_fields=None) -> List[dict]:
    telemetries = mongo.db.telemetry.find(query, output_fields)
    decrypted_list = []
    for telemetry in telemetries:
        try:
            decrypted_list.append(decrypt_dict(sensitive_fields, telemetry))
        except FieldNotFoundError:
            decrypted_list.append(telemetry)
    return decrypted_list
