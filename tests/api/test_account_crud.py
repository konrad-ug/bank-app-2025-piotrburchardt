from tests.api.conftest import BASE_URL


def test_create_account(client):
    payload = {"name": "james", "surname": "hetfield", "pesel": "89092909825"}

    response = client.post(f"{BASE_URL}/api/accounts", json=payload)

    assert response.status_code == 201
    assert response.json() == {"message": "Account created"}


def test_get_account_by_pesel(client):
    payload = {"name": "amy", "surname": "winehouse", "pesel": "93050999999"}
    client.post(f"{BASE_URL}/api/accounts", json=payload)

    response = client.get(f"{BASE_URL}/api/accounts/{payload['pesel']}")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["surname"] == payload["surname"]
    assert data["pesel"] == payload["pesel"]


def test_get_account_by_pesel_returns_404(client):
    response = client.get(f"{BASE_URL}/api/accounts/00000000000")

    assert response.status_code == 404


def test_update_account(client):
    payload = {"name": "old", "surname": "name", "pesel": "80101012345"}
    client.post(f"{BASE_URL}/api/accounts", json=payload)

    response = client.patch(f"{BASE_URL}/api/accounts/{payload['pesel']}", json={"name": "new"})

    assert response.status_code == 200
    assert response.json() == {"message": "Account updated"}

    get_response = client.get(f"{BASE_URL}/api/accounts/{payload['pesel']}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == "new"
    assert data["surname"] == payload["surname"]


def test_delete_account(client):
    payload = {"name": "delete", "surname": "me", "pesel": "75030344444"}
    client.post(f"{BASE_URL}/api/accounts", json=payload)

    delete_response = client.delete(f"{BASE_URL}/api/accounts/{payload['pesel']}")

    assert delete_response.status_code == 200
    follow_up = client.get(f"{BASE_URL}/api/accounts/{payload['pesel']}")
    assert follow_up.status_code == 404


def test_get_all_accounts_returns_empty_list(client):
    response = client.get(f"{BASE_URL}/api/accounts")

    assert response.status_code == 200
    assert response.json() == []


def test_get_account_count(client):
    payload = {"name": "count", "surname": "test", "pesel": "80010100000"}
    client.post(f"{BASE_URL}/api/accounts", json=payload)

    response = client.get(f"{BASE_URL}/api/accounts/count")

    assert response.status_code == 200
    assert response.json() == {"count": 1}


def test_update_account_returns_404_when_missing(client):
    response = client.patch(f"{BASE_URL}/api/accounts/99999999999", json={"name": "x"})

    assert response.status_code == 404


def test_delete_account_returns_404_when_missing(client):
    response = client.delete(f"{BASE_URL}/api/accounts/11111111111")

    assert response.status_code == 404


def test_create_account_with_duplicate_pesel_returns_409(client):
    payload = {"name": "dup", "surname": "test", "pesel": "70010112345"}
    client.post(f"{BASE_URL}/api/accounts", json=payload)

    response = client.post(f"{BASE_URL}/api/accounts", json=payload)

    assert response.status_code == 409
    assert response.json()["message"] == "Account with this pesel already exists"
