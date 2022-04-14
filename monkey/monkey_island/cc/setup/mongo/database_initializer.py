import json
import logging
from pathlib import Path
from pprint import pformat

from pymongo import errors

from monkey_island.cc.database import mongo
from monkey_island.cc.models.attack.attack_mitigations import AttackMitigations
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.services.database import Database

logger = logging.getLogger(__name__)

ATTACK_MITIGATION_PATH = (
    Path(MONKEY_ISLAND_ABS_PATH)
    / "cc"
    / "setup"
    / "mongo"
    / f"{AttackMitigations.COLLECTION_NAME}.json"
)


def reset_database():
    Database.reset_db()
    if Database.is_mitigations_missing():
        logger.info("Populating Monkey Island with ATT&CK mitigations.")
        _try_store_mitigations_on_mongo()


def _try_store_mitigations_on_mongo():
    mitigation_collection_name = AttackMitigations.COLLECTION_NAME
    try:
        mongo.db.validate_collection(mitigation_collection_name)
        if mongo.db.attack_mitigations.count_documents({}) == 0:
            raise errors.OperationFailure(
                "Mitigation collection empty. Try dropping the collection and running again"
            )
    except errors.OperationFailure:
        try:
            mongo.db.create_collection(mitigation_collection_name)
        except errors.CollectionInvalid:
            pass
        finally:
            _store_mitigations_on_mongo()


def _store_mitigations_on_mongo():
    try:
        with open(ATTACK_MITIGATION_PATH) as f:
            attack_mitigations = json.load(f)

        logger.debug(f'Loading attack mitigations data:\n{pformat(attack_mitigations["metadata"])}')

        mongodb_collection = mongo.db[AttackMitigations.COLLECTION_NAME]
        mongodb_collection.insert_many(attack_mitigations["data"])
    except json.decoder.JSONDecodeError as e:
        raise Exception(f"Invalid attack mitigations {ATTACK_MITIGATION_PATH} file: {e}")
