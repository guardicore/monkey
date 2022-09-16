import json
from typing import Callable, Iterable

from common.agent_event_serializers import JSONSerializable
from common.agent_events import AbstractAgentEvent

ENCRYPTED_PREFIX = "encrypted_"


def get_fields_to_encrypt(event: AbstractAgentEvent):
    """
    Get the fields of the event that are not part of the base AbstractAgentEvent.
    """
    return set(vars(AbstractAgentEvent)["__fields__"].keys()) ^ set(event.dict().keys())


def encrypt_event(
    encrypt: Callable[[bytes], bytes],
    event_data: JSONSerializable,
    fields: Iterable[str] = [],
) -> JSONSerializable:
    """
    Encrypt a serialized AbstractAgentEvent

    The data is expected to be a dict. The encrypted fields will be given the
    prefix "encrypted_".

    :param encrypt: Callable used to encrypt data
    :param event_data: Serialized event to encrypt
    :param fields: Fields to encrypt
    :return: Serialized event with the fields encrypted
    :raises TypeError: If the serialized data is not a dict
    """
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
    """
    Decrypt a serialized AbstractEventData

    :param encrypt: Callable used to decrypt data
    :param event_data: Serialized event to decrypt
    :return: Serialized event with the fields decrypted
    :raises TypeError: If the serialized data is not a dict
    """
    if not isinstance(event_data, dict):
        raise TypeError("Event decryption only supported for dict")

    for field in event_data.keys():
        if field.startswith("encrypted_"):
            event_data[field[len(ENCRYPTED_PREFIX) :]] = json.loads(
                str(decrypt(event_data[field].encode()), "utf-8")
            )
            del event_data[field]

    return event_data
