import pytest

from src.account import Account

class TestAccount:
    @pytest.mark.parametrize(
        "first_name,last_name,pesel,expected_pesel",
        [
            ("John", "Doe", "123", "Invalid"),
            ("Jane", "Doe", "01234567891", "01234567891"),
        ],
    )
    def test_account_creation(self, first_name, last_name, pesel, expected_pesel):
        account = Account(first_name, last_name, pesel)

        assert account.first_name == first_name
        assert account.last_name == last_name
        assert account.balance == 0.0
        assert account.pesel == expected_pesel

    @pytest.mark.parametrize(
        "pesel,promo_code,expected_balance,eligible",
        [
            ("05260000000", "PROM_123", 50.0, True),
            ("12345678912", None, 0.0, None),
            ("12345672212", "zly kod", 0.0, None),
            ("50010178912", "PROM_123", 0.0, False),
            ("123", "PROM_12345", 0.0, False),
        ],
    )
    def test_account_promo_flow(self, pesel, promo_code, expected_balance, eligible):
        acc = Account("John", "Doe", pesel, promo_code)

        assert acc.balance == expected_balance
        if eligible is not None:
            assert acc.is_eligible_for_promo() is eligible

    def test_get_birth_year_returns_zero_for_unknown_month(self):
        acc = Account("Sam", "Doe", "99130000000")

        assert acc.get_birth_year() == 00
