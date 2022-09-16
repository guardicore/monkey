import json
from typing import Callable, Iterable

from common.agent_event_serializers import JSONSerializable
from common.agent_events import AbstractAgentEvent

ENCRYPTED_PREFIX = "encrypted_"


def get_fields_to_encrypt(event: AbstractAgentEvent):
    return set(vars(AbstractAgentEvent)["__fields__"].keys()) ^ set(event.dict().keys())


def encrypt_event(
    encrypt: Callable[[bytes], bytes],
    event_data: JSONSerializable,
    fields: Iterable[str] = [],
) -> JSONSerializable:
    if not isinstance(event_data, dict):
        raise TypeError("Event encryption only supported for dict")

    for field in fields:
        event_data[ENCRYPTED_PREFIX + field] = str(
            encrypt(json.dumps(event_data[field]).encode()), "utf-8"
        )
        del event_data[field]

    return event_data


def decrypt_event(
    decrypt: Callable[[bytes], bytes], event_data: JSONSerializable
) -> JSONSerializable:
    if not isinstance(event_data, dict):
        raise TypeError("Event decryption only supported for dict")

    for field in event_data.keys():
        if field.startswith("encrypted_"):
            event_data[field[len(ENCRYPTED_PREFIX) :]] = json.loads(
                str(decrypt(event_data[field].encode()), "utf-8")
            )
            del event_data[field]

    return event_data
