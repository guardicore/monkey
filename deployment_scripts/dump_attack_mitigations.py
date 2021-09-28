import argparse

import pymongo


def main():
    args = parse_args()
    mongodb = connect_to_mongo(args.mongo_host, args.mongo_port, args.database_name)

    clean_collection(mongodb, args.collection_name)


def parse_args():
    parser = argparse.ArgumentParser(description="Export attack mitigations from a database")
    parser.add_argument(
        "-host", "--mongo_host", default="localhost", help="URL for mongo database.", required=False
    )
    parser.add_argument(
        "-port",
        "--mongo_port",
        action="store",
        default=27017,
        type=int,
        help="Port for mongo database. Default 27017",
        required=False,
    )
    parser.add_argument(
        "-db",
        "--database_name",
        action="store",
        default="monkeyisland",
        help="Database name inside of mongo.",
        required=False,
    )
    parser.add_argument(
        "-cn",
        "--collection_name",
        action="store",
        default="attack_mitigations",
        help="Which collection are we going to export",
        required=False,
    )
    return parser.parse_args()


def connect_to_mongo(mongo_host: str, mongo_port: int, database_name: str) -> pymongo.MongoClient:
    client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
    database = client.get_database(database_name)
    return database


def clean_collection(mongodb: pymongo.MongoClient, collection_name: str):
    if collection_exists(mongodb, collection_name):
        mongodb.drop_collection(collection_name)


def collection_exists(mongodb: pymongo.MongoClient, collection_name: str) -> bool:
    collections = mongodb.list_collection_names()
    return collection_name in collections


if __name__ == "__main__":
    main()
