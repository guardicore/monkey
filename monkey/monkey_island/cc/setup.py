from monkey_island.cc.services.attack.mitre_api_interface import MitreApiInterface
from monkey_island.cc.models.attack_mitigation import AttackMitigation
from monkey_island.cc.database import mongo
from pymongo import errors


def setup():
    try_store_mitigations_on_mongo()


def try_store_mitigations_on_mongo():
    # import the 'errors' module from PyMongo
    mitigation_collection_name = 'attack_mitigation'
    try:
        mongo.db.validate_collection(mitigation_collection_name)
    except errors.OperationFailure:
        mongo.db.create_collection(mitigation_collection_name)
        store_mitigations_on_mongo()


def store_mitigations_on_mongo():
    all_mitigations = MitreApiInterface.get_all_mitigations()
    for mitigation in all_mitigations:
        AttackMitigation.add_mitigation_from_stix2(mitigation)
