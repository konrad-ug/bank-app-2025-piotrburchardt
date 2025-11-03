from src.account import Account


class TestAccountTransfers:
    def test_transfer_increases_balance(self):
        account = Account("John", "Doe", "05260000000")
        result = account.transfer_in(100)

        assert result is True
        assert account.balance == 100

    def test_transfer_out_decreases_balance(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(100)

        result = account.transfer_out(40)

        assert result is True
        assert account.balance == 60

    def test_transfer_out_fails_when_insufficient_balance(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(50)

        result = account.transfer_out(60)

        assert result is False
        assert account.balance == 50

    def test_transfer_in_fails_for_non_positive_amount(self):
        account = Account("John", "Doe", "05260000000")

        result = account.transfer_in(0)

        assert result is False
        assert account.balance == 0

    def test_transfer_out_fails_for_non_positive_amount(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(30)

        result = account.transfer_out(-10)

        assert result is False
        assert account.balance == 30

    def test_express_transfer_charges_fee(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(100)

        result = account.express_transfer_out(100)

        assert result is True
        assert account.balance == -1.0

    def test_express_transfer_fails_without_funds(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(40)

        result = account.express_transfer_out(50)

        assert result is False
        assert account.balance == 40

    def test_express_transfer_fails_for_non_positive_amount(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(30)

        result = account.express_transfer_out(0)

        assert result is False
        assert account.balance == 30