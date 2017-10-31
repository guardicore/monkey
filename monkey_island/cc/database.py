from flask_pymongo import PyMongo
from flask_pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

__author__ = 'Barak'

mongo = PyMongo()


def is_db_server_up(mongo_url):
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=100)
    try:
        client.server_info()
        return True
    except ServerSelectionTimeoutError:
        return False
