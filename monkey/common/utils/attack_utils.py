from enum import Enum


class ScanStatus(Enum):
    # Technique was attempted/scanned
    SCANNED = 1
    # Technique was attempted and succeeded
    USED = 2
