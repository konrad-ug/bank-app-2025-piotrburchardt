from datetime import date

import pytest

from src.account import Account, BusinessAccount


@pytest.mark.parametrize(
    "account_factory, history, expected_text",
    [
        (lambda: Account("John", "Doe", "05260000000"), [100, -1, 500], "Personal account history: [100, -1, 500]"),
        (lambda: BusinessAccount("Acme", "1234567890"), [5000, -1000, 500], "Company account history: [5000, -1000, 500]"),
    ],
)
def test_send_history_via_email_calls_smtp_with_subject_and_history(
    mocker, account_factory, history, expected_text
):
    account = account_factory()
    account.history = history
    mock_date = mocker.patch("src.account.date")
    mock_date.today.return_value = date(2025, 12, 30)
    mock_send = mocker.patch("src.account.SMTPClient.send", return_value=True)

    result = account.send_history_via_email("user@example.com")

    assert result is True
    mock_send.assert_called_once_with(
        "Account Transfer History 2025-12-30",
        expected_text,
        "user@example.com",
    )


@pytest.mark.parametrize(
    "account_factory",
    [
        lambda: Account("John", "Doe", "05260000000"),
        lambda: BusinessAccount("Acme", "1234567890"),
    ],
)
def test_send_history_via_email_returns_false_when_sending_fails(mocker, account_factory):
    account = account_factory()
    mock_date = mocker.patch("src.account.date")
    mock_date.today.return_value = date(2025, 12, 30)
    mock_send = mocker.patch("src.account.SMTPClient.send", return_value=False)

    result = account.send_history_via_email("user@example.com")

    assert result is False
    mock_send.assert_called_once()
