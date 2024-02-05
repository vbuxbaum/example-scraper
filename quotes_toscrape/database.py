import os
from pymongo import MongoClient
from pymongo.collection import Collection
from quotes_toscrape.entities import Quote, StoredQuote

db_client = MongoClient(os.environ.get("MONGODB_URI"))

db = db_client["quotes_db"]


class QuotesRepository:
    _collection: Collection = db["quotes"]

    @classmethod
    def insert_many(cls, quotes: list[Quote]):
        cls._collection.insert_many([quote.__dict__ for quote in quotes])

    @classmethod
    def find_all(cls, query={}) -> list[StoredQuote]:
        return [
            StoredQuote(_id=str(doc.pop("_id")), **doc)
            for doc in cls._collection.find(query)
        ]
