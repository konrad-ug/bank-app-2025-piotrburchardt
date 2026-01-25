import os
import time

import requests

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
TIMEOUT_SECONDS = 0.5


def _timed_request(session, method, path, **kwargs):
    start = time.monotonic()
    response = session.request(
        method,
        f"{BASE_URL}{path}",
        timeout=TIMEOUT_SECONDS,
        **kwargs,
    )
    elapsed = time.monotonic() - start
    assert elapsed < TIMEOUT_SECONDS
    return response


def test_create_and_delete_account_100_times():
    session = requests.Session()

    for i in range(100):
        pesel = f"990101{i:05d}"
        payload = {"name": "perf", "surname": "test", "pesel": pesel}

        response = _timed_request(session, "POST", "/api/accounts", json=payload)
        assert response.status_code == 201

        response = _timed_request(session, "DELETE", f"/api/accounts/{pesel}")
        assert response.status_code == 200


def test_100_incoming_transfers_and_balance():
    session = requests.Session()
    pesel = "88010112345"
    payload = {"name": "perf", "surname": "transfer", "pesel": pesel}

    response = _timed_request(session, "POST", "/api/accounts", json=payload)
    assert response.status_code == 201

    amount = 10
    for _ in range(100):
        response = _timed_request(
            session,
            "POST",
            f"/api/accounts/{pesel}/transfer",
            json={"amount": amount, "type": "incoming"},
        )
        assert response.status_code == 200

    response = _timed_request(session, "GET", f"/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()["balance"] == amount * 100
