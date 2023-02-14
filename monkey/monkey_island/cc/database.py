import gridfs
from flask_pymongo import PyMongo

mongo = PyMongo()


class Database:
    def __init__(self):
        self.gridfs = None

    def init(self):
        self.gridfs = gridfs.GridFS(mongo.db)


database = Database()
