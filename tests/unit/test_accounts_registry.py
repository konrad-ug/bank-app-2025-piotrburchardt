import pytest


class TestAccountsRegistry:
    def test_add_account_increases_count(self, accounts_registry, personal_account):
        assert accounts_registry.get_accounts_count() == 0

        accounts_registry.add_account(personal_account)

        assert accounts_registry.get_accounts_count() == 1

    @pytest.mark.parametrize(
        "lookup_pesel, expected_index",
        [
            ("05260111111", 1),
            ("00000000000", None),
        ],
    )
    def test_get_account_by_pesel(
        self, accounts_registry, sample_accounts, lookup_pesel, expected_index
    ):
        for account in sample_accounts:
            accounts_registry.add_account(account)

        result = accounts_registry.get_account_by_pesel(lookup_pesel)

        if expected_index is None:
            assert result is None
        else:
            assert result is sample_accounts[expected_index]

    def test_get_all_accounts_returns_copy(self, accounts_registry, sample_accounts):
        for account in sample_accounts:
            accounts_registry.add_account(account)

        accounts = accounts_registry.get_all_accounts()
        accounts.pop()

        assert accounts_registry.get_accounts_count() == len(sample_accounts)
        assert (
            accounts_registry.get_account_by_pesel(sample_accounts[1].pesel)
            is sample_accounts[1]
        )
