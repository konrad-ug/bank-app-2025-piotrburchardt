from src.account import Account

class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "123")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "Invalid" or len(account.pesel) == 11

    def test_account_stores_valid_pesel(self):
        valid_pesel = "01234567891"
        account = Account("Jane", "Doe", valid_pesel)

        assert account.pesel == valid_pesel

    def test_account_with_valid_promo(self):
        acc = Account("John", "Doe", "05260000000", "PROM_123")
        assert acc.balance == 50.0

    def test_account_without_promo(self):
        acc = Account("Jan", "Doe", "12345678912")
        assert acc.balance == 0.0

    def test_account_with_invalid_promo(self):
        acc = Account("John", "Doe", "12345672212", "zly kod")
        assert acc.balance == 0.0

    def test_account_with_valid_promo_but_too_old(self):
        acc = Account("John", "Old", "50010178912", "PROM_123")
        assert acc.balance == 0.0
