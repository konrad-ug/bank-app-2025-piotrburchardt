import os

import pytest
import requests
from pymongo import MongoClient

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000").rstrip("/")


@pytest.fixture
def client():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(autouse=True)
def clear_registry(client):
    response = client.get(f"{BASE_URL}/api/accounts")
    if response.ok:
        for account in response.json():
            client.delete(f"{BASE_URL}/api/accounts/{account['pesel']}")


@pytest.fixture(autouse=True)
def clear_database():
    client = MongoClient("mongodb://localhost:27017")
    client["bank_app"]["accounts"].delete_many({})
    yield
    client["bank_app"]["accounts"].delete_many({})
    client.close()
