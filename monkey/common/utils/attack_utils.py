from enum import Enum


class ScanStatus(Enum):
    # Technique wasn't scanned
    UNSCANNED = 0
    # Technique was attempted/scanned
    SCANNED = 1
    # Technique was attempted and succeeded
    USED = 2
    # Techique was disabled
    DISABLED = 3


class UsageEnum(Enum):
    SMB = {ScanStatus.USED.value: "SMB exploiter ran the monkey by creating a service via MS-SCMR.",
           ScanStatus.SCANNED.value: "SMB exploiter failed to run the monkey by creating a service via MS-SCMR."}
    MIMIKATZ = {ScanStatus.USED.value: "Windows module loader was used to load Mimikatz DLL.",
                ScanStatus.SCANNED.value: "Monkey tried to load Mimikatz DLL, but failed."}
    MIMIKATZ_WINAPI = {ScanStatus.USED.value: "WinAPI was called to load mimikatz.",
                       ScanStatus.SCANNED.value: "Monkey tried to call WinAPI to load mimikatz."}
    DROPPER = {ScanStatus.USED.value: "WinAPI was used to mark monkey files for deletion on next boot."}
    SINGLETON_WINAPI = {ScanStatus.USED.value: "WinAPI was called to acquire system singleton for monkey's process.",
                        ScanStatus.SCANNED.value: "WinAPI call to acquire system singleton"
                                                  " for monkey process wasn't successful."}
    DROPPER_WINAPI = {ScanStatus.USED.value: "WinAPI was used to mark monkey files for deletion on next boot."}


# Dict that describes what BITS job was used for
BITS_UPLOAD_STRING = "BITS job was used to upload monkey to a remote system."


def format_time(time):
    return "%s-%s %s:%s:%s" % (time.date().month,
                               time.date().day,
                               time.time().hour,
                               time.time().minute,
                               time.time().second)
