from enum import Enum


class ScanStatus(Enum):
    # Technique wasn't scanned
    UNSCANNED = 0
    # Technique was attempted/scanned
    SCANNED = 1
    # Technique was attempted and succeeded
    USED = 2


# Dict that describes what BITS job was used for
BITS_UPLOAD_STRING = "BITS job was used to upload agent to a remote system."
