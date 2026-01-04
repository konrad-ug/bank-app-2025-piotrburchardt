import pytest

from src.account import Account, AccountsRegistry, BusinessAccount


@pytest.fixture
def personal_account():
    return Account("John", "Doe", "05260000000")


@pytest.fixture
def business_account():
    return BusinessAccount("Acme", "1234567890")


@pytest.fixture
def accounts_registry():
    return AccountsRegistry()


@pytest.fixture
def sample_accounts():
    return (
        Account("John", "Doe", "05260000000"),
        Account("Jane", "Doe", "05260111111"),
    )


@pytest.fixture(autouse=True)
def mock_mf_request(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": {"subject": {"statusVat": "Czynny"}}
    }
    return mocker.patch("src.account.requests.get", return_value=mock_response)
