import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from Expense import Expense
from ExpenseManager import ExpenseManager
from chart_drawer import draw_category_chart
from email_sender import send_expense_report
from currency_converter import convert_currency
from tkinter import simpledialog


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Dashboard")
        self.root.geometry("800x550")
        self.root.configure(bg="#f0f4f8")
        self.manager = ExpenseManager()

        # Set Style
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TLabel', background='#f0f4f8', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('TLabelframe', background='#dfe7ed', padding=10)
        self.style.configure('TLabelframe.Label', font=('Segoe UI', 12, 'bold'))
        self.style.configure('TEntry', padding=4)
        self.manager = ExpenseManager(csv_path="expenses.csv")

        # Title Label
        title_label = tk.Label(root, text="📊 Personal Finance Dashboard",
                               font=("Segoe UI", 16, "bold"), bg="#f0f4f8", fg="#333")
        title_label.pack(pady=10)

        # Input Frame
        input_frame = ttk.LabelFrame(root, text="Add New Expense")
        input_frame.pack(fill="x", padx=20, pady=10)

        # Amount
        ttk.Label(input_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Category
        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.category_entry = ttk.Entry(input_frame, width=15)
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        # Currency
        ttk.Label(input_frame, text="Currency:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.currency_entry = ttk.Entry(input_frame, width=15)
        self.currency_entry.grid(row=1, column=1, padx=5, pady=5)

        # Description
        ttk.Label(input_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(input_frame, width=15)
        self.description_entry.grid(row=1, column=3, padx=5, pady=5)

        # Date
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Add Button
        self.add_button = ttk.Button(input_frame, text="➕ Add Expense", command=self.add_expense)
        self.add_button.grid(row=2, column=3, padx=5, pady=5, sticky="e")

        # Button Frame
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="📂 Load CSV", command=self.load_csv).grid(row=0, column=0, padx=12)
        ttk.Button(button_frame, text="💾 Save CSV", command=self.save_csv).grid(row=0, column=1, padx=12)
        ttk.Button(button_frame, text="📈 View Charts", command=self.view_charts).grid(row=0, column=2, padx=12)
        ttk.Button(button_frame, text="📝 Generate Report", command=self.generate_report).grid(row=0, column=3, padx=12)
        ttk.Button(button_frame, text="✉️ Send Email", command=self.send_email).grid(row=0, column=4, padx=12)
        ttk.Button(button_frame, text="💱 Convert Currency", command=self.convert_total_currency).grid(row=0, column=5,padx=12)
        ttk.Button(button_frame, text="📅 Filter by Date", command=self.filter_by_date).grid(row=0, column=6, padx=5)

        # Expenses List
        list_frame = ttk.LabelFrame(root, text="Expenses")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.expenses_list = tk.Listbox(list_frame, height=12, font=('Segoe UI', 10), bg="#ffffff", fg="#333")
        self.expenses_list.pack(fill="both", expand=True, padx=5, pady=5)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            currency = self.currency_entry.get()
            date = self.date_entry.get()
            description = self.description_entry.get()

            expense = Expense(amount, category, currency, date, description)
            self.manager.add_expense(expense)
            self.expenses_list.insert(tk.END, str(expense))

            # Clear inputs
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.currency_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
            self.manager.add_expense(expense)
            self.manager.save_to_csv("expenses.csv")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def save_csv(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]

        )
        if filepath:
            self.manager.save_to_csv(filepath)
            messagebox.showinfo("Success", f"Expenses saved to:\n{filepath}")

    def load_csv(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]

        )
        if filepath:
            self.manager.load_from_csv(filepath)
            self.expenses_list.delete(0, tk.END)
            for expense in self.manager.expenses:
                self.expenses_list.insert(tk.END, str(expense))
            messagebox.showinfo("Success", f"Expenses loaded from:\n{filepath}")


    def generate_report(self):
        messagebox.showinfo("Generate Report", "This will generate a report (to be implemented).")

    def send_email(self):
        messagebox.showinfo("Send Email", "This will send an email with report (to be implemented).")

    def view_charts(self):
        if not self.manager.expenses:
            messagebox.showinfo("No Data", "No expenses to show.")
            return

        # Summarize by category
        category_totals = {}
        for expense in self.manager.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

        draw_category_chart(category_totals)

    def send_email(self):
        if not self.manager.expenses:
            messagebox.showinfo("No Data", "No expenses to send!")
            return

        # Ask user where to save CSV first
        filepath = filedialog.asksaveasfilename(defaultextension=".csv")
        if not filepath:
            return

        # Save the CSV
        self.manager.save_to_csv(filepath)

        # Prompt user for email details
        email_window = tk.Toplevel(self.root)
        email_window.title("Send Email")

        tk.Label(email_window, text="Sender Email:").grid(row=0, column=0, sticky="e")
        sender_entry = tk.Entry(email_window, width=40)
        sender_entry.grid(row=0, column=1)

        tk.Label(email_window, text="Password / App Password:").grid(row=1, column=0, sticky="e")
        password_entry = tk.Entry(email_window, show="*", width=40)
        password_entry.grid(row=1, column=1)

        tk.Label(email_window, text="Recipient Email:").grid(row=2, column=0, sticky="e")
        recipient_entry = tk.Entry(email_window, width=40)
        recipient_entry.grid(row=2, column=1)

        tk.Label(email_window, text="Subject:").grid(row=3, column=0, sticky="e")
        subject_entry = tk.Entry(email_window, width=40)
        subject_entry.insert(0, "Expense Report")
        subject_entry.grid(row=3, column=1)

        tk.Label(email_window, text="Body:").grid(row=4, column=0, sticky="e")
        body_text = tk.Text(email_window, width=30, height=5)
        body_text.insert(tk.END, "Please find attached the expense report.")
        body_text.grid(row=4, column=1)

        def send_button_action():
            try:
                sender = sender_entry.get()
                password = password_entry.get()
                recipient = recipient_entry.get()
                subject = subject_entry.get()
                body = body_text.get("1.0", tk.END).strip()

                send_expense_report(
                    sender,
                    password,
                    recipient,
                    subject,
                    body,
                    filepath
                )

                messagebox.showinfo("Success", "Email sent successfully!")
                email_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email:\n{e}")

        send_button = tk.Button(email_window, text="Send Email", command=send_button_action)
        send_button.grid(row=5, column=0, columnspan=2, pady=10)

    def convert_total_currency(self):
        if not self.manager.expenses:
            messagebox.showinfo("No Data", "No expenses to convert!")
            return

        # Sum total expenses
        total_amount = sum(e.amount for e in self.manager.expenses)

        # Ask user for target currency
        def do_conversion():
            target_currency = currency_entry.get().upper().strip()
            if not target_currency:
                messagebox.showerror("Error", "Please enter a target currency code.")
                return
            try:
                converted = convert_currency(total_amount, "USD", target_currency)
                result_label.config(text=f"Total in {target_currency}: {converted:.2f}")
            except Exception as e:
                messagebox.showerror("Error", f"Conversion failed:\n{e}")

        # Build small dialog
        win = tk.Toplevel(self.root)
        win.title("Convert Currency")

        tk.Label(win, text=f"Total in USD: {total_amount:.2f}").grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(win, text="Target Currency (e.g. EUR, INR):").grid(row=1, column=0, sticky="e")
        currency_entry = tk.Entry(win)
        currency_entry.grid(row=1, column=1)

        convert_button = tk.Button(win, text="Convert", command=do_conversion)
        convert_button.grid(row=2, column=0, columnspan=2, pady=5)

        result_label = tk.Label(win, text="")
        result_label.grid(row=3, column=0, columnspan=2, pady=5)

    def filter_by_date(self):
        if not self.manager.expenses:
            messagebox.showinfo("No Data", "No expenses to filter!")
            return

        # Ask for start and end date
        filter_win = tk.Toplevel(self.root)
        filter_win.title("Filter Expenses by Date")

        tk.Label(filter_win, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e")
        start_entry = tk.Entry(filter_win)
        start_entry.grid(row=0, column=1)

        tk.Label(filter_win, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="e")
        end_entry = tk.Entry(filter_win)
        end_entry.grid(row=1, column=1)

        result_text = tk.Text(filter_win, width=40, height=10)
        result_text.grid(row=3, column=0, columnspan=2, pady=5)

        def apply_filter():
            start_str = start_entry.get().strip()
            end_str = end_entry.get().strip()
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date()

                filtered_expenses = self.manager.filter_by_date(start_date, end_date)

                if not filtered_expenses:
                    result_text.delete("1.0", tk.END)
                    result_text.insert(tk.END, "No expenses in this date range.")
                    return

                total = sum(e.amount for e in filtered_expenses)
                summary = self.manager.summarize_by_category(filtered_expenses)

                # Show results
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, f"Total in range: ${total:.2f}\n\n")
                result_text.insert(tk.END, "Category breakdown:\n")
                for cat, amt in summary.items():
                    result_text.insert(tk.END, f"  {cat}: ${amt:.2f}\n")

            except Exception as e:
                messagebox.showerror("Error", f"Invalid date or filtering error:\n{e}")

        tk.Button(filter_win, text="Apply Filter", command=apply_filter).grid(row=2, column=0, columnspan=2, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
