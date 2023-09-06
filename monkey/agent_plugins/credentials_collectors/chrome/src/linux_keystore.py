# Utilities for connecting to chrome secret storage

import logging
import os
from binascii import hexlify
from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from typing import Iterator, Optional, Set, Tuple

import dbus
import psutil
import secretstorage

# Override jeepney.auth.make_auth_external so that we can connect to a session with uid
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
        bus = _connect_to_dbus_session(uid, session)
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
def _get_dbus_sessions(setenv=True) -> Iterator[Tuple[str, str]]:
    visited = set()
    for process in psutil.process_iter():
        try:
            environ = process.environ()
        except Exception:
            continue

        if "DBUS_SESSION_BUS_ADDRESS" not in environ:
            continue

        address = environ["DBUS_SESSION_BUS_ADDRESS"]

        if address not in visited:
            uid = process.uids().effective
            previous = None
            previous_uid = None

            if setenv:
                previous_uid = os.geteuid()

                if not uid == previous_uid:
                    try:
                        os.seteuid(uid)
                    except Exception:
                        continue

                if "DBUS_SESSION_BUS_ADDRESS" in os.environ:
                    previous = os.environ["DBUS_SESSION_BUS_ADDRESS"]

                os.environ["DBUS_SESSION_BUS_ADDRESS"] = address

            try:
                yield (uid, address)
            except Exception:
                pass
            finally:
                if setenv:
                    if previous:
                        os.environ["DBUS_SESSION_BUS_ADDRESS"] = previous
                    else:
                        del os.environ["DBUS_SESSION_BUS_ADDRESS"]

                    if previous_uid != uid:
                        try:
                            os.seteuid(previous_uid)
                        except Exception:
                            pass

                visited.add(address)


# TODO: Determine if we need to connect to an existing session by uid, DBUS_SESSION_BUS_ADDRESS
def _connect_to_dbus_session(uid: str, session: str) -> Optional[secretstorage.DBusConnection]:
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
