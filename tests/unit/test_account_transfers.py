import pytest


class TestAccountTransfers:
    def test_transfer_increases_balance(self, personal_account):
        result = personal_account.transfer_in(100)

        assert result is True
        assert personal_account.balance == 100

    def test_transfer_out_decreases_balance(self, personal_account):
        personal_account.transfer_in(100)

        result = personal_account.transfer_out(40)

        assert result is True
        assert personal_account.balance == 60

    @pytest.mark.parametrize(
        "deposit, withdraw_amount, expected_balance",
        [
            (50, 60, 50),
            (30, -10, 30),
        ],
    )
    def test_transfer_out_fails(
        self, personal_account, deposit, withdraw_amount, expected_balance
    ):
        personal_account.transfer_in(deposit)

        result = personal_account.transfer_out(withdraw_amount)

        assert result is False
        assert personal_account.balance == expected_balance

    def test_transfer_in_fails_for_non_positive_amount(self, personal_account):
        result = personal_account.transfer_in(0)

        assert result is False
        assert personal_account.balance == 0

    def test_express_transfer_charges_fee(self, personal_account):
        personal_account.transfer_in(100)

        result = personal_account.express_transfer_out(100)

        assert result is True
        assert personal_account.balance == -1.0

    def test_express_transfer_fails_without_funds(self, personal_account):
        personal_account.transfer_in(40)

        result = personal_account.express_transfer_out(50)

        assert result is False
        assert personal_account.balance == 40

    def test_express_transfer_fails_for_non_positive_amount(self, personal_account):
        personal_account.transfer_in(30)

        result = personal_account.express_transfer_out(0)

        assert result is False
        assert personal_account.balance == 30
