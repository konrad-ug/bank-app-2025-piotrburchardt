import pytest


class TestBusinessAccountLoans:
    @pytest.mark.parametrize(
        "operations, loan_amount, expected_result, expected_balance",
        [
            (
                [("transfer_in", 3000), ("transfer_out", 1775)],
                700,
                False,
                1225,
            ),
            (
                [("transfer_in", 5000)],
                2000,
                False,
                5000,
            ),
            (
                [("transfer_in", 5000), ("transfer_out", 1775)],
                1500,
                True,
                4725,
            ),
            (
                [("transfer_in", 4000), ("transfer_out", 1775)],
                0,
                False,
                2225,
            ),
        ],
    )
    def test_business_account_loan_conditions(
        self, business_account, operations, loan_amount, expected_result, expected_balance
    ):
        for operation, amount in operations:
            getattr(business_account, operation)(amount)

        result = business_account.submit_for_loan(loan_amount)

        assert result is expected_result
        assert business_account.balance == expected_balance
