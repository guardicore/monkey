"""
File that contains ATT&CK telemetry storing/retrieving logic
"""
import logging
from cc.database import mongo
from time import time

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
    mongo.db.attack_results.update({'name': 'latest'}, {'name': 'latest', 'timestamp': time()}, upsert=True)


def get_latest_telem():
    return mongo.db.attack_results.find_one({'name': 'latest'})
