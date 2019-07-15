from enum import Enum


class ScanStatus(Enum):
    # Technique wasn't scanned
    UNSCANNED = 0
    # Technique was attempted/scanned
    SCANNED = 1
    # Technique was attempted and succeeded
    USED = 2


class UsageEnum(Enum):
    SMB = {ScanStatus.USED.value: "SMB exploiter ran the monkey by creating a service via MS-SCMR.",
           ScanStatus.SCANNED.value: "SMB exploiter failed to run the monkey by creating a service via MS-SCMR."}
    MIMIKATZ = {ScanStatus.USED.value: "Windows module loader was used to load Mimikatz DLL.",
                ScanStatus.SCANNED.value: "Monkey tried to load Mimikatz DLL, but failed."}


# Dict that describes what BITS job was used for
BITS_UPLOAD_STRING = "BITS job was used to upload monkey to a remote system."


def format_time(time):
    return "%s-%s %s:%s:%s" % (time.date().month,
                               time.date().day,
                               time.time().hour,
                               time.time().minute,
                               time.time().second)
