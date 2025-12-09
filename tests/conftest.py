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
