import sqlite3
from datetime import datetime

import pandas as pd


def create_database():
    """Create SQLite database and tables"""
    conn = sqlite3.connect("kaas.db")
    cursor = conn.cursor()

    # Create transaction_past table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS transactions_past (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        description TEXT,
        category TEXT,
        amount DECIMAL(10,2),
        related_account TEXT,
        status TEXT
    )
    """
    )

    # Create accounts_present table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS accounts_present (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_name TEXT,
        current_balance DECIMAL(10,2)
    )
    """
    )

    # Create freedom_future table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS freedom_future (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        planned_date DATE,
        description TEXT,
        category TEXT,
        expected_amount DECIMAL(10,2),
        frequency TEXT,
        payment_method TEXT,
        status TEXT
    )
    """
    )

    conn.commit()
    return conn


def clean_transaction_past(df):
    # Expected columns for transaction_past
    required_cols = [
        "date",
        "description",
        "category",
        "amount",
        "related_account",
        "status",
    ]

    # Rename columns if they exist with different names
    rename_map = {
        "SLNo": None,  # Drop this column
        "Date": "date",
        "Description": "description",
        "Category": "category",
        "Amount": "amount",
        "Related Account": "related_account",
        "Status": "status",
    }

    # Rename columns and drop unnecessary ones
    df = df.rename(columns=rename_map)

    # Drop any columns that map to None
    df = df.drop(
        [col for col, val in rename_map.items() if val is None], axis=1, errors="ignore"
    )

    return df


def clean_accounts_present(df):
    # Expected columns for accounts_present
    required_cols = ["account_name", "current_balance"]

    # Rename columns if they exist with different names
    rename_map = {
        "SLNo": None,  # Drop this column
        "Account Name": "account_name",
        "Current Balance": "current_balance",
    }

    # Rename columns and drop unnecessary ones
    df = df.rename(columns=rename_map)

    # Drop any columns that map to None
    df = df.drop(
        [col for col, val in rename_map.items() if val is None], axis=1, errors="ignore"
    )

    return df


def clean_freedom_future(df):
    # Expected columns for freedom_future
    required_cols = [
        "planned_date",
        "description",
        "category",
        "expected_amount",
        "frequency",
        "payment_method",
        "status",
    ]

    # Rename columns if they exist with different names
    rename_map = {
        "SLNo": None,  # Drop this column
        "Planned Date": "planned_date",
        "Description": "description",
        "Category": "category",
        "Expected Amount": "expected_amount",
        "Frequency": "frequency",
        "Payment Method": "payment_method",
        "Status": "status",
    }

    # Rename columns and drop unnecessary ones
    df = df.rename(columns=rename_map)

    # Drop any columns that map to None
    df = df.drop(
        [col for col, val in rename_map.items() if val is None], axis=1, errors="ignore"
    )

    return df


def import_excel_data(excel_path):
    try:
        xls = pd.ExcelFile(excel_path)
        conn = create_database()

        # Mapping of sheet names to cleaning functions
        cleaning_functions = {
            "Transactions_Past": clean_transaction_past,
            "Accounts_Present": clean_accounts_present,
            "freedom_future": clean_freedom_future,
        }

        # Import all sheets
        for sheet_name in xls.sheet_names:
            # Convert sheet name to SQLite table name convention
            table_name = sheet_name.lower().replace(" ", "_").replace("-", "_")

            # Read the sheet
            df = pd.read_excel(xls, sheet_name)

            # Clean the dataframe if we have a cleaning function for it
            if sheet_name in cleaning_functions:
                df = cleaning_functions[sheet_name](df)

            # Create table and import data
            print(f"Importing {sheet_name} as {table_name}...")
            df.to_sql(table_name, conn, if_exists="replace", index=False)

        conn.commit()
        conn.close()
        print("Data imported successfully!")

    except Exception as e:
        print(f"Error importing data: {str(e)}")
        raise  # Re-raise the exception to see the full traceback


if __name__ == "__main__":
    excel_path = "DB/bkp/Kaas_24Feb25.xlsm"
    import_excel_data(excel_path)
