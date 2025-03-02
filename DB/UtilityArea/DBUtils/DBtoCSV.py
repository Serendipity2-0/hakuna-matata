import sqlite3
import pandas as pd
import os
import pathlib

def sqlite_to_csv(db_path: str) -> None:
    """
    Convert all tables in a SQLite database to CSV files.
    
    Args:
        db_path: Path to the SQLite database file
    """
    # Get database name without extension
    db_name = pathlib.Path(db_path).stem
    
    # Create output directory
    output_dir = os.path.join('DB/CSV', db_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    try:
        # Get list of all tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Convert each table to CSV
        for table in tables:
            table_name = table[0]
            
            # Read table into pandas DataFrame
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            
            # Save to CSV
            csv_path = os.path.join(output_dir, f"{table_name}.csv")
            df.to_csv(csv_path, index=False)
            print(f"Exported {table_name} to {csv_path}")
            
    finally:
        conn.close()
    
    print(f"\nAll tables from {db_path} have been exported to {output_dir}/")

if __name__ == "__main__":
    sqlite_to_csv("DB/main/kaas_24Feb.db")