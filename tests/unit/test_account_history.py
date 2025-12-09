import pytest

from src.account import Account


@pytest.fixture
def history_account():
    return Account("john", "johhny", "321")

class TestAccount:
    def test_account_history_in(self, history_account):
        history_account.transfer_in(100)
        history_account.transfer_in(100)
        history_account.transfer_in(30)

        assert history_account.history[0] == 100
        assert history_account.history[1] == 100
        assert history_account.history[2] == 30

    def test_account_history_in_and_out(self, history_account):
        history_account.transfer_in(100)
        history_account.transfer_in(1000)
        history_account.transfer_out(100)

        assert history_account.history[0] == 100
        assert history_account.history[1] == 1000
        assert history_account.history[2] == -100

    def test_account_history_empty(self, history_account):
        assert not history_account.history

    def test_account_history_expressTransfer(self, history_account):
        history_account.transfer_in(200)
        history_account.transfer_in(100)
        history_account.express_transfer_out(100)

        assert history_account.history[0] == 200
        assert history_account.history[1] == 100
        assert history_account.history[2] == -100
        assert history_account.history[3] == -1
