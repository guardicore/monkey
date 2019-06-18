import gridfs
from flask_pymongo import MongoClient, PyMongo
from pymongo.errors import ServerSelectionTimeoutError

__author__ = 'Barak'

mongo = PyMongo()


class Database:
    def __init__(self):
        self.gridfs = None

    def init(self):
        self.gridfs = gridfs.GridFS(mongo.db)


database = Database()


def is_db_server_up(mongo_url):
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=100)
    try:
        client.server_info()
        return True
    except ServerSelectionTimeoutError:
        return False


def get_db_version(mongo_url):
    """
    Return the mongo db version
    :param mongo_url: Which mongo to check.
    :return: version as a tuple (e.g. `(u'4', u'0', u'8')`)
    """
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=100)
    server_version = tuple(client.server_info()['version'].split('.'))
    return server_version
