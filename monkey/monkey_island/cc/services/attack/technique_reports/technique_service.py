from cc.database import mongo
from common.utils.attack_status_enum import ScanStatus

__author__ = "VakarisZ"


def technique_status(technique):
    if mongo.db.attack_results.find_one({'status': ScanStatus.USED.value, 'technique': technique}):
        return ScanStatus.USED
    elif mongo.db.attack_results.find_one({'status': ScanStatus.SCANNED.value, 'technique': technique}):
        return ScanStatus.SCANNED
    else:
        return ScanStatus.UNSCANNED


def technique_title(technique):
    return technique+" title from SCHEMA"
