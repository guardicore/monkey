# Utilities for connecting to chrome secret storage

import logging
from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from typing import Iterator, Set, Tuple

import secretstorage


@dataclass
class EncryptionConfig:
    length: int
    salt: bytes
    iterations: int


logger = logging.getLogger(__name__)

ENC_CONFIG = EncryptionConfig(
    length=16,
    salt=b"saltysalt",
    iterations=1,
)


def get_decryption_keys_from_storage() -> Iterator[bytes]:
    used_session_labels: Set[str] = set()
    for uid, session in _get_dbus_sessions():
        bus = _connect_to_dbus_session(uid, session)
        for collection in secretstorage.get_all_collections(bus):
            yield from _get_secrets_from_collection(collection, used_session_labels)


def _get_secrets_from_collection(
    collection: secretstorage.collection.Collection,
    used_session_labels: Set[str],
) -> Iterator[bytes]:
    if collection.is_locked():
        return

    label = collection.get_label()
    if label in used_session_labels:
        return
    used_session_labels.add(label)

    for item in collection.get_all_items():
        if item.get_label().endswith("Safe Storage"):
            yield _hash_decryption_key(item.get_secret())


def _hash_decryption_key(key: bytes):
    decryption_key = pbkdf2_hmac(
        hash_name="sha1",
        password=key,
        salt=ENC_CONFIG.salt,
        iterations=ENC_CONFIG.iterations,
        dklen=ENC_CONFIG.length,
    )
    return decryption_key


# TODO: Determine if we need to get the uid, DBUS_SESSION_BUS_ADDRESS from the environment
def _get_dbus_sessions() -> Iterator[Tuple[str, str]]:
    yield ("uid", "session")


# TODO: Determine if we need to connect to an existing session by uid, DBUS_SESSION_BUS_ADDRESS
def _connect_to_dbus_session(uid: str, session: str) -> secretstorage.dbus.SessionBus:
    return secretstorage.dbus_init()
