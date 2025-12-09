import threading

import pytest
import requests
from werkzeug.serving import make_server

from app.api import app, registry


@pytest.fixture(scope="module")
def api_url():
    server = make_server("127.0.0.1", 5001, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    yield "http://127.0.0.1:5001"

    server.shutdown()
    thread.join()


@pytest.fixture(autouse=True)
def clear_registry():
    registry.accounts.clear()


def test_create_account(api_url):
    payload = {"name": "james", "surname": "hetfield", "pesel": "89092909825"}

    response = requests.post(f"{api_url}/api/accounts", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["surname"] == payload["surname"]
    assert data["pesel"] == payload["pesel"]
    assert "balance" in data


def test_get_account_by_pesel(api_url):
    payload = {"name": "amy", "surname": "winehouse", "pesel": "93050999999"}
    requests.post(f"{api_url}/api/accounts", json=payload)

    response = requests.get(f"{api_url}/api/accounts/{payload['pesel']}")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["surname"] == payload["surname"]
    assert data["pesel"] == payload["pesel"]


def test_get_account_by_pesel_returns_404(api_url):
    response = requests.get(f"{api_url}/api/accounts/00000000000")

    assert response.status_code == 404


def test_update_account(api_url):
    payload = {"name": "old", "surname": "name", "pesel": "80101012345"}
    requests.post(f"{api_url}/api/accounts", json=payload)

    response = requests.patch(
        f"{api_url}/api/accounts/{payload['pesel']}", json={"name": "new"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "new"
    assert data["surname"] == payload["surname"]


def test_delete_account(api_url):
    payload = {"name": "delete", "surname": "me", "pesel": "75030344444"}
    requests.post(f"{api_url}/api/accounts", json=payload)

    delete_response = requests.delete(f"{api_url}/api/accounts/{payload['pesel']}")

    assert delete_response.status_code == 200
    follow_up = requests.get(f"{api_url}/api/accounts/{payload['pesel']}")
    assert follow_up.status_code == 404


def test_get_all_accounts_returns_empty_list(api_url):
    response = requests.get(f"{api_url}/api/accounts")

    assert response.status_code == 200
    assert response.json() == []


def test_get_account_count(api_url):
    payload = {"name": "count", "surname": "test", "pesel": "80010100000"}
    requests.post(f"{api_url}/api/accounts", json=payload)

    response = requests.get(f"{api_url}/api/accounts/count")

    assert response.status_code == 200
    assert response.json() == {"count": 1}


def test_create_account_missing_fields_returns_400(api_url):
    response = requests.post(f"{api_url}/api/accounts", json={"name": "only"})

    assert response.status_code == 400


def test_create_business_account_requires_fields(api_url):
    response = requests.post(f"{api_url}/api/accounts", json={"type": "business"})

    assert response.status_code == 400


def test_update_account_returns_404_when_missing(api_url):
    response = requests.patch(f"{api_url}/api/accounts/99999999999", json={"name": "x"})

    assert response.status_code == 404


def test_update_business_account(api_url):
    from src.account import BusinessAccount

    account = BusinessAccount("OldCo", "1234567890")
    account.pesel = "BIZ00000001"
    registry.add_account(account)

    response = requests.patch(
        f"{api_url}/api/accounts/{account.pesel}", json={"company_name": "NewCo"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "NewCo"


def test_create_business_account(api_url):
    payload = {"type": "business", "company_name": "Biz", "nip": "1234567890"}

    response = requests.post(f"{api_url}/api/accounts", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "business"
    assert data["nip"] == payload["nip"]


def test_delete_account_returns_404_when_missing(api_url):
    response = requests.delete(f"{api_url}/api/accounts/11111111111")

    assert response.status_code == 404
