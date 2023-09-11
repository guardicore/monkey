# Utilities for connecting to chrome secret storage

import logging
import os
from binascii import hexlify
from contextlib import contextmanager
from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from typing import Iterator, Optional, Set, Tuple

import dbus
import psutil
import secretstorage

# Override jeepney.auth.make_auth_external so that we can connect to a session with uid
# Each process in Unix has specific UID of the user that owns the process.
# In order for processes to communicate over D-BUS IPC system there is a D-BUS auth
# which requires the UID. Jeepney.auth uses os.geteuid but we need to be able to connect
# to D-BUS using other users ID so we override make_auth_external
# https://jeepney.readthedocs.io/en/latest/_modules/jeepney/auth.html#make_auth_external
try:
    import jeepney.auth
except Exception:
    pass
else:

    def make_auth_external():
        hex_uid = hexlify(str(make_auth_external.uid).encode("ascii"))
        return b"AUTH EXTERNAL %b\r\n" % hex_uid

    jeepney.auth.make_auth_external = make_auth_external


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
        with _dbus_session(uid, session) as bus:
            if bus is None:
                continue
            try:
                for collection in secretstorage.get_all_collections(bus):
                    yield from _get_secrets_from_collection(collection, used_session_labels)
            except secretstorage.exceptions.SecretServiceNotAvailableException:
                logger.warning("Secret service not available")
                continue


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
            yield hash_decryption_key(item.get_secret())


def hash_decryption_key(key: bytes):
    decryption_key = pbkdf2_hmac(
        hash_name="sha1",
        password=key,
        salt=ENC_CONFIG.salt,
        iterations=ENC_CONFIG.iterations,
        dklen=ENC_CONFIG.length,
    )
    return decryption_key


def _get_dbus_sessions() -> Iterator[Tuple[int, str]]:
    processed_addresses = set()
    for process in psutil.process_iter():
        try:
            address = _get_dbus_session_address(process)
        except Exception:
            continue

        if address not in processed_addresses:
            uid = process.uids().effective

            yield (uid, address)

            processed_addresses.add(address)


@contextmanager
def _dbus_session(uid: int, address: str):
    previous_uid = None
    previous_address = None
    try:
        previous_uid = _set_uid(uid)
        previous_address = _set_session_address(address)
    except Exception:
        return

    try:
        yield _connect_to_dbus_session(uid, address)
    except Exception:
        pass
    finally:
        _revert_session_environment(previous_uid, previous_address)


def _get_dbus_session_address(process) -> str:
    environ = process.environ()
    if "DBUS_SESSION_BUS_ADDRESS" not in environ:
        raise Exception(f"No sessions found for PID {process.pid}")

    return environ["DBUS_SESSION_BUS_ADDRESS"]


def _revert_session_environment(previous_uid: int, previous_address: str):
    try:
        _set_uid(previous_uid)
    except Exception:
        pass
    _set_session_address(previous_address)


def _set_uid(uid: int):
    previous_uid = os.geteuid()
    if uid != previous_uid:
        os.seteuid(uid)
    return previous_uid


def _set_session_address(session: Optional[str]):
    previous_address = None
    if "DBUS_SESSION_BUS_ADDRESS" in os.environ:
        previous_address = os.environ["DBUS_SESSION_BUS_ADDRESS"]

    if session is None:
        del os.environ["DBUS_SESSION_BUS_ADDRESS"]
    else:
        os.environ["DBUS_SESSION_BUS_ADDRESS"] = session

    return previous_address


def _connect_to_dbus_session(uid: int, session: str) -> Optional[secretstorage.DBusConnection]:
    try:
        # List bus connection names
        bus = dbus.bus.BusConnection(session)
        if "org.freedesktop.secrets" not in [str(x) for x in bus.list_names()]:
            logger.debug("No secret service found")
            return None
    except Exception:
        logger.debug("Failed to query to dbus session")
        return None

    try:
        from jeepney.io.blocking import open_dbus_connection

        make_auth_external.uid = uid
        return open_dbus_connection(session)
    except Exception:
        logger.debug("Failed to connect to dbus session")
        return None
