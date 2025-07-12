from datetime import datetime

class Expense:
    def __init__(self, amount, category, currency, date, description):
        self.amount = amount
        self.category = category
        self.currency = currency
        self.date = date
        self.description = description

    def __str__(self):
        return f"{self.amount:.2f} {self.currency} - {self.category} - {self.description} ({self.date})"

    def to_dict(self):
        return {
            "Amount": self.amount,
            "Category": self.category,
            "Currency": self.currency,
            "Date": self.date,
            "Description": self.description
        }
