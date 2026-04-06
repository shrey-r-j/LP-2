import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime

# ---------- Account / state ----------
balance = 10000.00
transactions = []

account_details = {
    "name": "Sharv Mahajan",
    "account_no": "1234567890",
    "bank": "ABC Bank",
    "branch": "Mumbai"
}

# ---------- Helper functions ----------
def parse_amount(text):
    """
    Extract first numeric amount from text.
    Supports commas and decimals, e.g. "deposit 2,500.50" -> 2500.50
    Returns float or None if no valid amount.
    """
    m = re.search(r'([0-9]{1,3}(?:[,\d]*)(?:\.\d+)?)', text.replace('₹',''))
    if not m:
        return None
    num_str = m.group(1).replace(',', '')
    try:
        return float(num_str)
    except ValueError:
        return None

def fmt_amt(a):
    """Format amount with two decimals and commas, with ₹ sign."""
    return f"₹{a:,.2f}"

def add_transaction(desc):
    """Record transaction with timestamp, keep only last 10."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transactions.append((ts, desc))
    # keep last 10
    while len(transactions) > 10:
        transactions.pop(0)

def append_chat(speaker, message):
    """Insert a message into the chat box (read-only) and autoscroll."""
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, f"{speaker} ({datetime.now().strftime('%H:%M:%S')}):\n")
    chat.insert(tk.END, f"{message}\n\n")
    chat.see(tk.END)
    chat.config(state=tk.DISABLED)

# ---------- Bot logic ----------
def bot_response_text(user_text):
    global balance
    text = user_text.lower().strip()

    commands = {
        "deposit": ["deposit", "add", "credit"],
        "withdraw": ["withdraw", "take", "debit"],
        "balance": ["balance", "amount", "bal"],
        "transactions": ["transactions", "history", "statement", "transactions"],
        "account": ["account", "details", "info"]
    }

    # find command
    for cmd, keys in commands.items():
        if any(k in text for k in keys):
            if cmd == "deposit":
                amount = parse_amount(text)
                if amount is None or amount <= 0:
                    return "Please specify a valid amount to deposit, e.g. 'deposit 2000' or 'deposit 2,000.50'."
                balance += amount
                add_transaction(f"Deposited {fmt_amt(amount)}")
                return f"{fmt_amt(amount)} deposited successfully.\nCurrent balance: {fmt_amt(balance)}"

            elif cmd == "withdraw":
                amount = parse_amount(text)
                if amount is None or amount <= 0:
                    return "Please specify a valid amount to withdraw, e.g. 'withdraw 500'."
                if amount > balance:
                    return f"Insufficient balance. Your current balance is {fmt_amt(balance)}."
                balance -= amount
                add_transaction(f"Withdrew {fmt_amt(amount)}")
                return f"{fmt_amt(amount)} withdrawn successfully.\nCurrent balance: {fmt_amt(balance)}"

            elif cmd == "balance":
                return f"Your current balance is {fmt_amt(balance)}."

            elif cmd == "transactions":
                if not transactions:
                    return "No transactions yet."
                lines = [f"{ts} — {desc}" for ts, desc in transactions[-10:]]
                return "Last transactions (latest last):\n" + "\n".join(lines)

            elif cmd == "account":
                return (f"Name: {account_details['name']}\n"
                        f"Account No: {account_details['account_no']}\n"
                        f"Bank: {account_details['bank']}\n"
                        f"Branch: {account_details['branch']}")

    # fallback
    return ("I can help with: deposit <amount>, withdraw <amount>, balance, "
            "transactions, account details. Example: 'deposit 2000' or 'withdraw 500'.")

# ---------- UI actions ----------
def send_message(event=None):
    user_input = entry.get().strip()
    if not user_input:
        return  # ignore empty
    # show user message
    append_chat("You", user_input)
    entry.delete(0, tk.END)

    # get bot response
    resp = bot_response_text(user_input)
    append_chat("Bot", resp)

def on_balance_click():
    append_chat("You", "balance")
    append_chat("Bot", bot_response_text("balance"))

def on_transactions_click():
    append_chat("You", "transactions")
    append_chat("Bot", bot_response_text("transactions"))

def on_account_click():
    append_chat("You", "account")
    append_chat("Bot", bot_response_text("account"))

def on_clear_click():
    if messagebox.askyesno("Clear chat", "Clear the chat history?"):
        chat.config(state=tk.NORMAL)
        chat.delete('1.0', tk.END)
        chat.config(state=tk.DISABLED)

# ---------- Build GUI ----------
root = tk.Tk()
root.title("Banking Chatbot - ABC Bank")
root.geometry("520x560")
root.minsize(420, 400)

# Layout with grid: row 0 = chat (expandable), row 1 = input (fixed height), row 2 = buttons (fixed)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Chat Text with scrollbar (read-only)
chat_frame = tk.Frame(root)
chat_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
chat_frame.rowconfigure(0, weight=1)
chat_frame.columnconfigure(0, weight=1)

chat = tk.Text(chat_frame, wrap=tk.WORD, state=tk.DISABLED)
vsb = tk.Scrollbar(chat_frame, orient=tk.VERTICAL, command=chat.yview)
chat.configure(yscrollcommand=vsb.set)

chat.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")

# Input row (fixed height)
input_frame = tk.Frame(root)
input_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(0,8))
input_frame.columnconfigure(0, weight=1)

entry = tk.Entry(input_frame, font=("Arial", 12))
entry.grid(row=0, column=0, sticky="ew", padx=(0,6), ipady=4)  # ipady -> keeps entry a bit taller but fixed
send_btn = tk.Button(input_frame, text="Send", width=10, command=send_message)
send_btn.grid(row=0, column=1, sticky="e")

# Quick-action buttons (fixed)
btn_frame = tk.Frame(root)
btn_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=(0,8))
for i in range(4):
    btn_frame.columnconfigure(i, weight=1)

balance_btn = tk.Button(btn_frame, text="Balance", command=on_balance_click)
trans_btn = tk.Button(btn_frame, text="Transactions", command=on_transactions_click)
acct_btn = tk.Button(btn_frame, text="Account", command=on_account_click)
clear_btn = tk.Button(btn_frame, text="Clear Chat", command=on_clear_click)

balance_btn.grid(row=0, column=0, sticky="ew", padx=4)
trans_btn.grid(row=0, column=1, sticky="ew", padx=4)
acct_btn.grid(row=0, column=2, sticky="ew", padx=4)
clear_btn.grid(row=0, column=3, sticky="ew", padx=4)

# Bind Enter to send_message; allow Shift+Enter to insert newline (rarely used since Entry is single-line)
def entry_return(event):
    if (event.state & 0x1) != 0:
        return
    send_message()
    return "break"  # prevent default behavior

entry.bind("<Return>", entry_return)
entry.focus_set()

append_chat("Bot", f"Welcome {account_details['name']}! I can help with deposit, withdraw, balance, transactions, or account details.\nTry: 'deposit 2000' or 'withdraw 500'.")

root.mainloop()