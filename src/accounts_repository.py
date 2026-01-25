from pymongo import MongoClient

from src.account import Account


class MongoAccountsRepository:
    def __init__(self, collection=None, uri="mongodb://localhost:27017", db_name="bank_app", collection_name="accounts"):
        if collection is None:
            client = MongoClient(uri)
            self._collection = client[db_name][collection_name]
        else:
            self._collection = collection

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            data = {
                "first_name": getattr(account, "first_name", None),
                "last_name": getattr(account, "last_name", None),
                "pesel": getattr(account, "pesel", None),
                "balance": getattr(account, "balance", 0.0),
                "history": getattr(account, "history", []),
            }
            self._collection.update_one({"pesel": data["pesel"]}, {"$set": data}, upsert=True)

    def load_all(self):
        accounts = []
        for document in self._collection.find():
            account = Account(document.get("first_name"), document.get("last_name"), document.get("pesel"))
            account.balance = document.get("balance", 0.0)
            account.history = document.get("history", [])
            accounts.append(account)
        return accounts
