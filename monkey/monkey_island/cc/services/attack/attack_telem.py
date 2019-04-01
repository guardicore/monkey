"""
File that contains ATT&CK telemetry storing/retrieving logic
"""
import logging
from cc.database import mongo

__author__ = "VakarisZ"

logger = logging.getLogger(__name__)


def set_results(technique, data):
    data.update({'technique': technique})
    mongo.db.attack_results.insert(data)
