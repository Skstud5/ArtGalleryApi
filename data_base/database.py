import os
from pymongo import MongoClient
from pymongo.database import Database as MongoDBDatabase

MONGODB_URL = os.getenv("DATABASE_URL")
MONGODB_DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGODB_URL)
mongo_db: MongoDBDatabase = client[MONGODB_DATABASE_NAME]


def get_db() -> MongoDBDatabase:
    return mongo_db
