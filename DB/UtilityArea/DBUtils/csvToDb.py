# Help me convert csv files in a given directory to sqlite database

import sqlite3
import os

import pandas as pd

def csv_to_db(csv_dir: str, db_path: str):
    # Get list of all csv files in directory
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    
    # Create sqlite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables for each csv file
    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (")
        
        # Read csv file
        df = pd.read_csv(os.path.join(csv_dir, csv_file))
        
        # Get column names
        columns = df.columns.tolist()
        
        # Add columns to table
        for column in columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column} TEXT")
        
        # Insert data into table
        for index, row in df.iterrows():
            cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join([f"'{str(row[col])}'" for col in columns])})")
        
        # Commit changes
        conn.commit()
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    csv_to_db("DB/CSV/Calendar", "DB/bkp/Calendar.db")