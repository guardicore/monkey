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
from ctypes.wintypes import BOOL, DWORD, HANDLE, HWND, LPCWSTR, LPVOID, LPWSTR


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


def _get_data(blobOut):
    cbData = blobOut.cbData
    pbData = blobOut.pbData
    buffer = create_string_buffer(cbData)
    memmove(buffer, pbData, sizeof(buffer))
    LocalFree(pbData)
    return buffer.raw


def win32crypt_unprotect_data(cipherText):
    decrypted = None

    bufferIn = c_buffer(cipherText, len(cipherText))
    blobIn = DATA_BLOB(len(cipherText), bufferIn)
    blobOut = DATA_BLOB()

    if CryptUnprotectData(byref(blobIn), None, None, None, None, 0, byref(blobOut)):
        decrypted = _get_data(blobOut)

    return decrypted
