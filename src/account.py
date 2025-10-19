class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
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