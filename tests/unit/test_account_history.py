from src.account import Account

class TestAccount:
    def test_account_history_in(self):
        account = Account("john", "johhny", "321")

        account.transfer_in(100)
        account.transfer_in(100)
        account.transfer_in(30)

        assert account.history[0] == 100
        assert account.history[1] == 100
        assert account.history[2] == 30

    def test_account_history_in_and_out(self):
        account = Account("john", "johhny", "321")

        account.transfer_in(100)
        account.transfer_in(1000)
        account.transfer_out(100)
    
        assert account.history[0] == 100
        assert account.history[1] == 1000
        assert account.history[2] == -100


    def test_account_history_empty(self):
        account = Account("john", "johhny", "321")

        assert not account.history

    def test_account_history_expressTransfer(self):
        account = Account("john", "johhny", "321")

        account.transfer_in(200)
        account.transfer_in(100)
        account.express_transfer_out(100)

        assert account.history[0] == 200
        assert account.history[1] == 100
        assert account.history[2] == -100
        assert account.history[3] == -1