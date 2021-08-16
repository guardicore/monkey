from mongoengine import connect

MONGO_DB_NAME = "monkeyisland"
MONGO_DB_HOST = "localhost"
MONGO_DB_PORT = 27017


def connect_dal_to_mongodb(db=MONGO_DB_NAME, host=MONGO_DB_HOST, port=MONGO_DB_PORT):
    connect(db=db, host=host, port=port)
