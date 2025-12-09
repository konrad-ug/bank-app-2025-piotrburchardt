import pytest


class TestAccountLoans:
    def test_declines_non_positive_amount(self, personal_account):
        personal_account.transfer_in(100)

        assert personal_account.submit_for_loan(0) is False
        assert personal_account.submit_for_loan(-50) is False
        assert personal_account.balance == 100

    def test_declines_with_fewer_than_three_transactions(self, personal_account):
        personal_account.transfer_in(100)

        result = personal_account.submit_for_loan(200)

        assert result is False
        assert personal_account.balance == 100

    def test_grants_when_last_three_transactions_are_deposits(self, personal_account):
        personal_account.transfer_in(100)
        personal_account.transfer_out(50)
        personal_account.transfer_in(20)
        personal_account.transfer_in(30)
        personal_account.transfer_in(40)

        result = personal_account.submit_for_loan(200)

        assert result is True
        assert personal_account.balance == 340

    def test_express_fee_counts_towards_history(self, personal_account):
        personal_account.transfer_in(100)
        personal_account.transfer_in(100)
        personal_account.transfer_in(100)
        personal_account.express_transfer_out(50)
        personal_account.transfer_in(200)
        personal_account.transfer_in(50)

        result = personal_account.submit_for_loan(350)

        assert result is False
        assert personal_account.balance == 499

    @pytest.mark.parametrize(
        "operations, loan_amount, expected_result, expected_balance",
        [
            (
                [
                    ("transfer_in", 500),
                    ("transfer_out", 100),
                    ("transfer_in", 200),
                    ("transfer_in", 200),
                    ("transfer_out", 50),
                    ("transfer_in", 150),
                ],
                350,
                True,
                1250,
            ),
            (
                [
                    ("transfer_in", 10),
                    ("transfer_in", 1),
                    ("transfer_out", 1),
                    ("transfer_in", 1),
                    ("transfer_out", 10),
                    ("transfer_in", 1),
                ],
                10000,
                False,
                2,
            ),
        ],
    )
    def test_decision_based_on_last_five_transactions(
        self, personal_account, operations, loan_amount, expected_result, expected_balance
    ):
        for operation, amount in operations:
            getattr(personal_account, operation)(amount)

        result = personal_account.submit_for_loan(loan_amount)

        assert result is expected_result
        assert personal_account.balance == expected_balance
