from src.account import Account


class TestAccountLoans:
    def test_declines_with_fewer_than_three_transactions(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(100)

        result = account.submit_for_loan(200)

        assert result is False
        assert account.balance == 100

    def test_grants_when_last_three_transactions_are_deposits(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(100)
        account.transfer_out(50)
        account.transfer_in(20)
        account.transfer_in(30)
        account.transfer_in(40)

        result = account.submit_for_loan(200)

        assert result is True
        assert account.balance == 340

    def test_express_fee_counts_towards_history(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(100)
        account.transfer_in(100)
        account.transfer_in(100)
        account.express_transfer_out(50)
        account.transfer_in(200)
        account.transfer_in(50)

        result = account.submit_for_loan(350)

        assert result is False
        assert account.balance == 449

    def test_grants_when_sum_of_last_five_exceeds_amount(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(500)
        account.transfer_out(100)
        account.transfer_in(200)
        account.transfer_in(200)
        account.transfer_out(50)
        account.transfer_in(150)

        result = account.submit_for_loan(350)

        assert result is True
        assert account.balance == 1250

    def test_declines_when_sum_of_last_five_is_not_enough(self):
        account = Account("John", "Doe", "05260000000")
        account.transfer_in(5)
        account.transfer_in(6)
        account.transfer_out(1)
        account.transfer_in(20)
        account.transfer_out(10)
        account.transfer_in(5)

        result = account.submit_for_loan(10000)

        assert result is False
        assert account.balance == 85
