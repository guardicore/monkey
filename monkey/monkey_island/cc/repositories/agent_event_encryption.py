import json
from typing import Callable

from monkeytypes import JSONSerializable

from common.agent_events import AbstractAgentEvent

ENCRYPTED_PREFIX = "encrypted_"
ABSTRACT_AGENT_EVENT_FIELDS = vars(AbstractAgentEvent)["__fields__"].keys()
SERIALIZED_EVENT_FIELDS = set(ABSTRACT_AGENT_EVENT_FIELDS) | set(["type"])


def encrypt_event(
    encrypt: Callable[[bytes], bytes],
    event_data: JSONSerializable,
) -> JSONSerializable:
    """
    Encrypt a serialized AbstractAgentEvent

    The data is expected to be a dict. The encrypted fields will be given the
    prefix "encrypted_".

    :param encrypt: Callable used to encrypt data
    :param event_data: Serialized event to encrypt
    :return: Serialized event with the fields encrypted
    :raises TypeError: If the serialized data is not a dict
    """
    if not isinstance(event_data, dict):
        raise TypeError("Event encryption only supported for dict")

    data = event_data.copy()
    fields_to_encrypt = SERIALIZED_EVENT_FIELDS ^ set(event_data.keys())
    for field in fields_to_encrypt:
        data[ENCRYPTED_PREFIX + field] = str(
            encrypt(json.dumps(event_data[field]).encode()), "utf-8"
        )
        del data[field]

    return data


def decrypt_event(
    decrypt: Callable[[bytes], bytes], event_data: JSONSerializable
) -> JSONSerializable:
    """
    Decrypt a serialized AbstractEventData

    :param decrypt: Callable used to decrypt data
    :param event_data: Serialized event to decrypt
    :return: Serialized event with the fields decrypted
    :raises TypeError: If the serialized data is not a dict
    """
    if not isinstance(event_data, dict):
        raise TypeError("Event decryption only supported for dict")

    data = event_data.copy()
    for field in event_data.keys():
        if field.startswith("encrypted_"):
            data[field[len(ENCRYPTED_PREFIX) :]] = json.loads(
                str(decrypt(event_data[field].encode()), "utf-8")
            )
            del data[field]

    return data
