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

        if promo_code and (promo_code[0:5] == "PROM_") and promo_code[-3:].isdigit() and len(promo_code) == 8 and int(pesel[0:2]) >= 60 :
            self.balance += 50.0