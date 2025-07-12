import pandas as pd
from Expense import Expense
from datetime import datetime

class ExpenseManager:
    def __init__(self, csv_path=None):
        self.expenses = []
        self.csv_path = csv_path

    def add_expense(self, expense):
        self.expenses.append(expense)
        if self.csv_path:
            self.save_to_csv(self.csv_path)

    def to_dataframe(self):
        return pd.DataFrame([e.to_dict() for e in self.expenses])

    def save_to_csv(self, filepath=None):
        if filepath is None:
            filepath = self.csv_path
        df = self.to_dataframe()
        df = df.drop_duplicates()
        df.to_csv(filepath, index=False)

    def load_from_csv(self, filepath=None):
        if filepath is None:
            filepath = self.csv_path
        df = pd.read_csv(filepath)
        self.expenses = []
        for _, row in df.iterrows():
            expense = Expense(
                amount=row['Amount'],
                category=row['Category'],
                currency=row['Currency'],
                date=row['Date'],
                description=row['Description']
            )
            self.add_expense(expense)

    def filter_by_date(self, start_date, end_date):
        return [
            e for e in self.expenses
            if start_date <= e.date <= end_date
        ]

    def summarize_by_category(self, expenses=None):
        if expenses is None:
            expenses = self.expenses

        summary = {}
        for e in expenses:
            summary[e.category] = summary.get(e.category, 0) + e.amount
        return summary
