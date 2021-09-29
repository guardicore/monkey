import logging

from pymongo import errors

from monkey_island.cc.database import mongo
from monkey_island.cc.models.attack.attack_mitigations import AttackMitigations
from monkey_island.cc.services.attack.mitre_api_interface import MitreApiInterface
from monkey_island.cc.services.database import Database

logger = logging.getLogger(__name__)


def reset_database():
    Database.reset_db()
    if Database.is_mitigations_missing():
        logger.info("Populating Monkey Island with ATT&CK mitigations.")
        _try_store_mitigations_on_mongo()


def _try_store_mitigations_on_mongo():
    mitigation_collection_name = AttackMitigations.COLLECTION_NAME
    try:
        mongo.db.validate_collection(mitigation_collection_name)
        if mongo.db.attack_mitigations.count() == 0:
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
    # TODO: import attack mitigations
    pass
