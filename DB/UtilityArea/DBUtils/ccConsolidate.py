import os
import csv
import re
import pandas as pd
from datetime import datetime
import glob
import sqlite3  # Add SQLite import


def extract_account_number(file_content):
    """Extract account number from file content"""
    account_match = re.search(r'"Accountno:","(\d+)"', file_content)
    if account_match:
        return account_match.group(1)
    return "Unknown"


def parse_date(date_str):
    """Parse date from various formats to standardized YYYY-MM-DD"""
    date_str = date_str.strip('"').strip()

    # Handle various date formats
    try:
        if "/" in date_str:
            return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
        elif "-" in date_str:
            # Could be DD-MMM-YY or DD-MON-YYYY
            try:
                return datetime.strptime(date_str, "%d-%b-%y").strftime("%Y-%m-%d")
            except:
                try:
                    return datetime.strptime(date_str, "%d-%B-%Y").strftime("%Y-%m-%d")
                except:
                    return date_str
        else:
            return date_str
    except:
        return date_str


def clean_amount(amount_str):
    """Clean and convert amount string to float"""
    if not amount_str:
        return 0.0

    # Remove quotes, commas, and spaces
    cleaned = amount_str.strip('"').strip().replace(",", "")

    # Handle CR marker in the amount field
    if cleaned.endswith("CR"):
        cleaned = "-" + cleaned[:-2].strip()

    try:
        return float(cleaned)
    except:
        return 0.0


def is_card_number_row(row):
    """Check if the row contains a card number"""
    if not row or len(row) == 0:
        return False

    card_pattern = re.compile(r"\d+X+\d+|000\d+\s*X+\s*\d+")
    return bool(card_pattern.match(row[0]))


def is_header_row(row):
    """Check if the row is a header row"""
    if not row or len(row) < 3:
        return False

    # Headers typically include these column names
    header_keywords = ["Date", "Sr.No.", "Transaction Details", "Amount"]
    matched_keywords = sum(
        1 for keyword in header_keywords if any(keyword in col for col in row)
    )

    return matched_keywords >= 2


def parse_cc_statement(file_path):
    """Parse a credit card statement CSV file and extract transactions"""
    transactions = []
    in_transaction_section = False
    headers = []

    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
        account_no = extract_account_number(file_content)

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            # Skip empty rows
            if not row or len(row) == 0 or not row[0]:
                continue

            # Check if we've reached the transaction section
            if row[0] == "Transaction Details:":
                in_transaction_section = True
                continue

            # Check if we've moved past the transaction section
            if in_transaction_section and (
                row[0].startswith("EMI Details:")
                or row[0].startswith("MESSAGE Details:")
            ):
                in_transaction_section = False
                continue

            # Process rows in the transaction section
            if in_transaction_section:
                # Identify header row
                if is_header_row(row):
                    headers = row
                    continue

                # Skip card number rows
                if is_card_number_row(row):
                    continue

                # Need at least date, description and amount for a valid transaction
                if (
                    len(row) >= 3
                    and headers
                    and row[0]
                    and not row[0].startswith('"Transaction')
                ):
                    # Prepare transaction data with proper column mapping
                    transaction = {
                        "Date": row[0] if len(row) > 0 else "",
                        "Sr.No.": row[1] if len(row) > 1 else "",
                        "Transaction Details": row[2] if len(row) > 2 else "",
                        "Reward Point Header": row[3] if len(row) > 3 else "",
                        "Intl.Amount": row[4] if len(row) > 4 else "",
                        "Amount(in Rs)": row[5] if len(row) > 5 else "",
                        "BillingAmountSign": row[6] if len(row) > 6 else "",
                        "Account No": account_no,
                        "Source File": os.path.basename(file_path),
                    }

                    # Only add if we have at least date and amount
                    if transaction["Date"] and transaction["Amount(in Rs)"]:
                        transactions.append(transaction)

    return transactions


def create_sqlite_db(db_path):
    """Create SQLite database and transactions table if it doesn't exist"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create transactions table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Sr_No TEXT,
        Transaction_Details TEXT,
        Reward_Point_Header TEXT,
        Intl_Amount TEXT,
        Amount_in_Rs TEXT,
        BillingAmountSign TEXT,
        Account_No TEXT,
        Source_File TEXT,
        Standardized_Date TEXT,
        Cleaned_Amount REAL,
        Transaction_Type TEXT,
        Standardized_Amount REAL
    )
    """
    )

    conn.commit()
    return conn


def consolidate_cc_statements(directory_path):
    """Consolidate all credit card statements in the directory"""
    # Get all CSV files in the directory
    file_paths = glob.glob(os.path.join(directory_path, "*.csv"))

    # Initialize an empty list for all transactions
    all_transactions = []

    # Track files processed and transaction counts for validation
    files_processed = []
    transaction_counts = {}

    # Process each file
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        print(f"Processing {file_name}...")

        transactions = parse_cc_statement(file_path)
        transaction_counts[file_name] = len(transactions)
        files_processed.append(file_name)

        all_transactions.extend(transactions)

    if not all_transactions:
        print("No transactions found in any files.")
        return None

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(all_transactions)

    # Basic data cleaning and normalization
    # Standardize date format
    df["Standardized Date"] = df["Date"].apply(parse_date)

    # Clean and standardize amounts
    df["Cleaned Amount"] = df["Amount(in Rs)"].apply(clean_amount)

    # Determine if credit or debit
    df["Transaction Type"] = df.apply(
        lambda row: (
            "Credit"
            if (
                row["BillingAmountSign"] == "CR"
                or row["BillingAmountSign"] == "-"
                or row["Cleaned Amount"] < 0
                or "PAYMENT RECEIVED" in str(row["Transaction Details"]).upper()
            )
            else "Debit"
        ),
        axis=1,
    )

    # Standardize amount (positive for debit, negative for credit)
    df["Standardized Amount"] = df.apply(
        lambda row: (
            -abs(row["Cleaned Amount"])
            if row["Transaction Type"] == "Credit"
            else abs(row["Cleaned Amount"])
        ),
        axis=1,
    )

    # Perform sanity checks
    print("\n=== Sanity Checks ===")
    print(f"Total files processed: {len(files_processed)}")
    print(f"Total transactions found: {len(df)}")

    # Check for transactions with zero amount
    zero_amounts = df[df["Standardized Amount"] == 0].shape[0]
    print(f"Transactions with zero amount: {zero_amounts}")

    # Check for transactions with missing dates
    missing_dates = df[df["Standardized Date"] == ""].shape[0]
    print(f"Transactions with missing/invalid dates: {missing_dates}")

    # Check for potential duplicates (same date, amount, and description)
    potential_duplicates = df[
        df.duplicated(
            subset=["Standardized Date", "Transaction Details", "Standardized Amount"],
            keep=False,
        )
    ]
    print(f"Potential duplicate transactions: {len(potential_duplicates)}")

    if len(potential_duplicates) > 0:
        print("\nSample of potential duplicates:")
        print(
            potential_duplicates[
                [
                    "Standardized Date",
                    "Transaction Details",
                    "Standardized Amount",
                    "Source File",
                ]
            ].head(5)
        )

    # Summarize by account number
    print("\nTransactions by Account:")
    account_summary = df.groupby("Account No").size()
    print(account_summary)

    # Summarize by file
    print("\nTransactions by File:")
    for file, count in transaction_counts.items():
        print(f"{file}: {count} transactions")

    # Summarize transaction types
    print("\nTransaction Type Summary:")
    type_summary = df.groupby("Transaction Type").agg(
        {"Standardized Amount": ["count", "sum"]}
    )
    print(type_summary)

    # Sort by date
    df_sorted = df.sort_values("Standardized Date")

    # Save to SQLite database instead of CSV
    db_path = os.path.join(
        os.path.dirname(directory_path), "consolidated_cc_transactions.db"
    )

    # Create database connection and table
    conn = create_sqlite_db(db_path)

    # Prepare DataFrame for SQLite
    # Replace column names with SQLite-friendly names (no spaces or parentheses)
    df_for_sql = df_sorted.copy()
    df_for_sql.columns = [
        col.replace(".", "_").replace("(", "_").replace(")", "_")
        for col in df_for_sql.columns
    ]

    # Insert data into SQLite database (replace the table if it exists)
    df_for_sql.to_sql("transactions", conn, if_exists="replace", index=False)

    # Close the database connection
    conn.close()

    print(f"\nConsolidated data saved to SQLite database: {db_path}")
    return df_sorted


# If running as a script
if __name__ == "__main__":
    directory_path = "DB/BankStatements/CCStatements"
    consolidate_cc_statements(directory_path)

