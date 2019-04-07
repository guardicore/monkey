"""
File that contains ATT&CK telemetry storing/retrieving logic
"""
import logging
from cc.database import mongo

__author__ = "VakarisZ"

logger = logging.getLogger(__name__)


def set_results(technique, data):
    """
    Adds ATT&CK technique results(telemetry) to the database
    :param technique: technique ID string e.g. T1110
    :param data: Data, relevant to the technique
    """
    data.update({'technique': technique})
    mongo.db.attack_results.insert(data)
