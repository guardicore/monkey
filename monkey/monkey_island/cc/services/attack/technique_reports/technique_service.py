from cc.database import mongo
from common.utils.attack_utils import ScanStatus
from cc.services.attack.attack_config import get_technique

__author__ = "VakarisZ"


def technique_status(technique):
    """
    Gets status of certain attack technique. If
    :param technique:
    :return:
    """
    if mongo.db.attack_results.find_one({'status': ScanStatus.USED.value, 'technique': technique}):
        return ScanStatus.USED
    elif mongo.db.attack_results.find_one({'status': ScanStatus.SCANNED.value, 'technique': technique}):
        return ScanStatus.SCANNED
    else:
        return ScanStatus.UNSCANNED


def technique_title(technique):
    return get_technique(technique)['title']


def get_tech_base_data(technique, messages):
    data = {}
    status = technique_status(technique)
    title = technique_title(technique)
    data.update({'status': status.name, 'title': title})
    if status == ScanStatus.UNSCANNED:
        data.update({'message': messages['unscanned']})
    elif status == ScanStatus.SCANNED:
        data.update({'message': messages['scanned']})
    else:
        data.update({'message': messages['used']})
    return data
