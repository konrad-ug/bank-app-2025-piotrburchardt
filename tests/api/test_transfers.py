import pytest
from app.api import app, registry


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_registry():
    registry.accounts.clear()


def _create_personal_account(client, pesel="71010111111"):
    payload = {"name": "test", "surname": "user", "pesel": pesel}
    client.post("/api/accounts", json=payload)
    return payload


def test_incoming_transfer_success(client):
    payload = _create_personal_account(client, "71010111111")

    response = client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": 500, "type": "incoming"},
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
    assert registry.get_account_by_pesel(payload["pesel"]).balance == 500


def test_outgoing_transfer_success(client):
    payload = _create_personal_account(client, "72020222222")
    client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": 200, "type": "incoming"},
    )

    response = client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": 50, "type": "outgoing"},
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
    assert registry.get_account_by_pesel(payload["pesel"]).balance == 150


def test_outgoing_transfer_insufficient_funds_returns_422(client):
    payload = _create_personal_account(client, "73030333333")

    response = client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": 100, "type": "outgoing"},
    )

    assert response.status_code == 422


def test_express_transfer_success(client):
    payload = _create_personal_account(client, "74040444444")
    client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": 100, "type": "incoming"},
    )

    response = client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": 50, "type": "express"},
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Zlecenie przyjęto do realizacji"
    assert registry.get_account_by_pesel(payload["pesel"]).balance == 49


def test_transfer_unknown_type_returns_400(client):
    payload = _create_personal_account(client, "75050555555")

    response = client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": 10, "type": "weird"},
    )

    assert response.status_code == 400


def test_express_transfer_insufficient_funds_returns_422(client):
    payload = _create_personal_account(client, "75555555555")

    response = client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": 50, "type": "express"},
    )

    assert response.status_code == 422


def test_transfer_for_missing_account_returns_404(client):
    response = client.post(
        "/api/accounts/00000000000/transfer",
        json={"amount": 10, "type": "incoming"},
    )

    assert response.status_code == 404


def test_transfer_invalid_amount_returns_400(client):
    payload = _create_personal_account(client, "76060666666")

    response = client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": "not-a-number", "type": "incoming"},
    )

    assert response.status_code == 400


def test_incoming_transfer_non_positive_returns_400(client):
    payload = _create_personal_account(client, "77070777777")

    response = client.post(
        f"/api/accounts/{payload['pesel']}/transfer",
        json={"amount": 0, "type": "incoming"},
    )

    assert response.status_code == 400
