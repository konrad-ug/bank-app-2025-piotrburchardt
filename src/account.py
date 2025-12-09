class BaseAccount:
    express_fee = 0.0

    def __init__(self):
        self.balance = 0.0
        self.history = []

    def transfer_in(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)
            return True
        return False

    def transfer_out(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.history.append(-1 * amount)
            return True
        return False

    def express_transfer_out(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount + self.express_fee
            self.history.append(-1 * amount)
            self.history.append(-1 * self.express_fee)
            return True
        return False


class Account(BaseAccount):
    express_fee = 1.0

    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.promo_code = promo_code

        if len(pesel) != 11:
            self.pesel = "Invalid"
        else:
            self.pesel = pesel

        if self.is_valid_promo(promo_code) and self.is_eligible_for_promo():
            self.balance += 50.0

    def is_valid_promo(self, promo_code):
        if promo_code is None:
            return False
        return promo_code[0:5] == "PROM_" and len(promo_code) > 5

    def is_eligible_for_promo(self):
        if self.pesel == "Invalid":
            return False
        year = self.get_birth_year()
        return year > 1960

    def get_birth_year(self):
        year = int(self.pesel[:2])
        month = int(self.pesel[2:4])
        if 1 <= month <= 12:
            return 1900 + year
        elif 21 <= month <= 32:
            return 2000 + year
        return 0

    def submit_for_loan(self, amount):
        if amount <= 0:
            return False

        history_len = len(self.history)

        if history_len >= 3:
            last_three = self.history[-3:]
            if all(txn > 0 for txn in last_three):
                self.balance += amount
                return True

        if history_len >= 5:
            last_five_sum = sum(self.history[-5:])
            if last_five_sum > amount:
                self.balance += amount
                return True
        return False

class BusinessAccount(BaseAccount):
    express_fee = 5.0

    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        if len(nip) == 10 and nip.isdigit():
            self.nip = nip
        else:
            self.nip = "Invalid"

    def submit_for_loan(self, amount):
        if amount <= 0:
            return False

        has_zus_payment = -1775 in self.history
        sufficient_balance = self.balance >= 2 * amount

        if has_zus_payment and sufficient_balance:
            self.balance += amount
            return True

        return False


class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def get_account_by_pesel(self, pesel):
        for account in self.accounts:
            if getattr(account, "pesel", None) == pesel:
                return account
        return None

    def get_all_accounts(self):
        return list(self.accounts)

    def get_accounts_count(self):
        return len(self.accounts)
