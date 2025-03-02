#!/usr/bin/env python3
"""
Script to extract transaction data from SBI credit card statements (PDF)
and store them in a SQLite database.
"""

import os
import sqlite3
import glob
import sys
import re
import datetime
from pathlib import Path

# Add parent directory to path to import from UtilityArea
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from existing utilities
from UtilityArea.DBUtils.pdfToCsv import (
    extract_tables_from_pdf,
)  # Assuming this function exists

# Define paths
PDF_DIR = "DB/BankStatements/SBICard"
DB_PATH = "sbi_cc_transactions.db"


def create_database():
    """Create SQLite database with appropriate schema"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS sbi_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        transaction_details TEXT,
        amount REAL,
        pdf_source TEXT,
        processed_date TEXT
    )
    """
    )

    conn.commit()
    return conn


def parse_date(date_str):
    """Parse date from SBI statement format to YYYY-MM-DD"""
    try:
        # Try DD-MM-YYYY format
        date_obj = datetime.datetime.strptime(date_str.strip(), "%d-%m-%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        try:
            # Try DD/MM/YYYY format
            date_obj = datetime.datetime.strptime(date_str.strip(), "%d/%m/%Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            print(f"Could not parse date: {date_str}")
            return date_str  # Return as-is if parsing fails


def parse_amount(amount_str):
    """Parse amount string to float"""
    try:
        # Remove currency symbols, commas, etc. and convert to float
        cleaned = re.sub(r"[^\d.-]", "", amount_str.strip())
        return float(cleaned)
    except ValueError:
        print(f"Could not parse amount: {amount_str}")
        return 0.0


def identify_transaction_rows(tables):
    """
    Identify rows in the extracted tables that contain transaction information.
    Returns a list of tuples (date, transaction_details, amount).
    """
    transactions = []

    for table in tables:
        for row in table:
            # Skip header rows, footers, and other non-transaction rows
            if len(row) < 3:
                continue

            # Check if first column looks like a date
            if isinstance(row[0], str) and re.match(
                r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}", row[0]
            ):
                date = parse_date(row[0])
                details = row[1] if len(row) > 1 else ""
                amount = parse_amount(row[2]) if len(row) > 2 else 0.0

                transactions.append((date, details, amount))

    return transactions


def process_pdf(pdf_path, conn):
    """Process a single PDF file and add transactions to database"""
    cursor = conn.cursor()
    pdf_filename = os.path.basename(pdf_path)
    processed_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Extract tables from PDF
    tables = extract_tables_from_pdf(pdf_path)

    # Identify and extract transaction rows
    transactions = identify_transaction_rows(tables)

    # Insert transactions into database
    for date, details, amount in transactions:
        cursor.execute(
            "INSERT INTO sbi_transactions (date, transaction_details, amount, pdf_source, processed_date) VALUES (?, ?, ?, ?, ?)",
            (date, details, amount, pdf_filename, processed_date),
        )

    conn.commit()
    return len(transactions)


def process_all_pdfs():
    """Process all PDF files in the specified directory"""
    # Create or connect to database
    conn = create_database()

    # Get all PDF files
    pdf_files = glob.glob(os.path.join(PDF_DIR, "*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {PDF_DIR}")
        conn.close()
        return

    total_transactions = 0
    for pdf_file in pdf_files:
        try:
            transactions_added = process_pdf(pdf_file, conn)
            total_transactions += transactions_added
            print(
                f"Processed {os.path.basename(pdf_file)}, added {transactions_added} transactions"
            )
        except Exception as e:
            print(f"Error processing {os.path.basename(pdf_file)}: {e}")

    conn.close()
    print(f"Total transactions added to database: {total_transactions}")
    print(f"Database saved to: {os.path.abspath(DB_PATH)}")


if __name__ == "__main__":
    process_all_pdfs()
