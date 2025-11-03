from src.account import BusinessAccount


class TestBusinessAccount:
    def test_business_account_stores_valid_nip(self):
        account = BusinessAccount("Acme", "1234567890")

        assert account.company_name == "Acme"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_business_account_marks_invalid_nip(self):
        account = BusinessAccount("Acme", "123")

        assert account.nip == "Invalid"

    def test_business_account_transfers(self):
        account = BusinessAccount("Acme", "1234567890")

        assert account.transfer_in(200) is True
        assert account.transfer_out(50) is True
        assert account.balance == 150

    def test_business_account_transfer_out_fails_with_low_balance(self):
        account = BusinessAccount("Acme", "1234567890")
        account.transfer_in(20)

        assert account.transfer_out(30) is False
        assert account.balance == 20

    def test_business_express_transfer_uses_higher_fee(self):
        account = BusinessAccount("Acme", "1234567890")
        account.transfer_in(100)

        result = account.express_transfer_out(100)

        assert result is True
        assert account.balance == -5.0