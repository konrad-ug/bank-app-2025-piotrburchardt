from tests.api.conftest import BASE_URL


def test_save_and_load_accounts_replaces_registry(client):
    saved_payload = {"name": "save", "surname": "me", "pesel": "81010100001"}
    client.post(f"{BASE_URL}/api/accounts", json=saved_payload)
    client.post(
        f"{BASE_URL}/api/accounts/{saved_payload['pesel']}/transfer",
        json={"amount": 120, "type": "incoming"},
    )

    save_response = client.post(f"{BASE_URL}/api/accounts/save")
    assert save_response.status_code == 200
    assert save_response.json()["message"] == "Accounts saved"

    extra_payload = {"name": "temp", "surname": "user", "pesel": "82020200002"}
    client.post(f"{BASE_URL}/api/accounts", json=extra_payload)

    load_response = client.post(f"{BASE_URL}/api/accounts/load")
    assert load_response.status_code == 200
    assert load_response.json()["message"] == "Accounts loaded"

    saved_account_resp = client.get(f"{BASE_URL}/api/accounts/{saved_payload['pesel']}")
    assert saved_account_resp.status_code == 200
    assert saved_account_resp.json()["balance"] == 120

    missing_account_resp = client.get(f"{BASE_URL}/api/accounts/{extra_payload['pesel']}")
    assert missing_account_resp.status_code == 404
