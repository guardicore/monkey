from typing import Iterable

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


def get_all_collections_in_mongo(mongo_client: MongoClient) -> Iterable[Collection]:
    collections = [
        collection
        for db in get_all_databases_in_mongo(mongo_client)
        for collection in get_all_collections_in_database(db)
    ]

    assert len(collections) > 0
    return collections


def get_all_databases_in_mongo(mongo_client) -> Iterable[Database]:
    return (mongo_client[db_name] for db_name in mongo_client.list_database_names())


def get_all_collections_in_database(db: Database) -> Iterable[Collection]:
    return (db[collection_name] for collection_name in db.list_collection_names())
