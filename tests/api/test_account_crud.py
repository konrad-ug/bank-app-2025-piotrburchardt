import pytest
from app.api import app, registry


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_registry():
    registry.accounts.clear()


def test_create_account(client):
    payload = {"name": "james", "surname": "hetfield", "pesel": "89092909825"}

    response = client.post("/api/accounts", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == payload["name"]
    assert data["surname"] == payload["surname"]
    assert data["pesel"] == payload["pesel"]
    assert "balance" in data


def test_get_account_by_pesel(client):
    payload = {"name": "amy", "surname": "winehouse", "pesel": "93050999999"}
    client.post("/api/accounts", json=payload)

    response = client.get(f"/api/accounts/{payload['pesel']}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == payload["name"]
    assert data["surname"] == payload["surname"]
    assert data["pesel"] == payload["pesel"]


def test_get_account_by_pesel_returns_404(client):
    response = client.get("/api/accounts/00000000000")

    assert response.status_code == 404


def test_update_account(client):
    payload = {"name": "old", "surname": "name", "pesel": "80101012345"}
    client.post("/api/accounts", json=payload)

    response = client.patch(f"/api/accounts/{payload['pesel']}", json={"name": "new"})

    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "new"
    assert data["surname"] == payload["surname"]


def test_delete_account(client):
    payload = {"name": "delete", "surname": "me", "pesel": "75030344444"}
    client.post("/api/accounts", json=payload)

    delete_response = client.delete(f"/api/accounts/{payload['pesel']}")

    assert delete_response.status_code == 200
    follow_up = client.get(f"/api/accounts/{payload['pesel']}")
    assert follow_up.status_code == 404


def test_get_all_accounts_returns_empty_list(client):
    response = client.get("/api/accounts")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_account_count(client):
    payload = {"name": "count", "surname": "test", "pesel": "80010100000"}
    client.post("/api/accounts", json=payload)

    response = client.get("/api/accounts/count")

    assert response.status_code == 200
    assert response.get_json() == {"count": 1}


def test_create_account_missing_fields_returns_400(client):
    response = client.post("/api/accounts", json={"name": "only"})

    assert response.status_code == 400


def test_create_business_account_requires_fields(client):
    response = client.post("/api/accounts", json={"type": "business"})

    assert response.status_code == 400


def test_update_account_returns_404_when_missing(client):
    response = client.patch("/api/accounts/99999999999", json={"name": "x"})

    assert response.status_code == 404


def test_update_business_account(client):
    from src.account import BusinessAccount

    account = BusinessAccount("OldCo", "1234567890")
    account.pesel = "BIZ00000001"
    registry.add_account(account)

    response = client.patch(
        f"/api/accounts/{account.pesel}", json={"company_name": "NewCo"}
    )

    assert response.status_code == 200
    assert response.get_json()["name"] == "NewCo"


def test_create_business_account(client):
    payload = {"type": "business", "company_name": "Biz", "nip": "1234567890"}

    response = client.post("/api/accounts", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["type"] == "business"
    assert data["nip"] == payload["nip"]


def test_delete_account_returns_404_when_missing(client):
    response = client.delete("/api/accounts/11111111111")

    assert response.status_code == 404


def test_create_account_with_duplicate_pesel_returns_409(client):
    payload = {"name": "dup", "surname": "test", "pesel": "70010112345"}
    client.post("/api/accounts", json=payload)

    response = client.post("/api/accounts", json=payload)

    assert response.status_code == 409
    assert response.get_json()["message"] == "Account with this pesel already exists"
