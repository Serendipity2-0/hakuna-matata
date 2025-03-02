import sqlite3
import pandas as pd
import csv
import os
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SqlWriter:
    def __init__(self, db_path: str):
        """
        Initialize SqlWriter with database path
        
        Args:
            db_path (str): Path to the SQLite database
        """
        self.db_path = db_path

    def csv_to_sqlite(self, csv_path: str, table_name: str, if_exists: str = 'append') -> bool:
        """
        Sync CSV data to SQLite table
        
        Args:
            csv_path (str): Path to the CSV file
            table_name (str): Name of the SQLite table
            if_exists (str): How to behave if table exists ('fail', 'replace', 'append')
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read CSV file
            df = pd.read_csv(csv_path, parse_dates=['Date'])
            
            # Connect to SQLite database
            conn = sqlite3.connect(self.db_path)
            
            # Write to SQLite
            df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            
            conn.close()
            print(f"Successfully synced {csv_path} to {table_name}")
            logger.info(f"Successfully synced {csv_path} to {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing CSV to SQLite: {str(e)}")
            return False

    def sqlite_to_csv(self, table_name: str, output_path: str, query: Optional[str] = None) -> bool:
        """
        Download SQLite table data to CSV
        
        Args:
            table_name (str): Name of the SQLite table
            output_path (str): Path where CSV will be saved
            query (str, optional): Custom SQL query to fetch data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Connect to SQLite database
            conn = sqlite3.connect(self.db_path)
            
            # Create query
            if query is None:
                query = f"SELECT * FROM '{table_name}'"
            
            # Read data into DataFrame
            df = pd.read_sql_query(query, conn)
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            
            conn.close()
            logger.info(f"Successfully exported {table_name} to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting SQLite to CSV: {str(e)}")
            return False

# Example usage:
if __name__ == "__main__":
    # Create instance
    sql_writer = SqlWriter("DB/kaas.db")
    
    # Example CSV to SQLite sync
    sql_writer.csv_to_sqlite("Utils/sample_freedom.csv", "Freedom(Future)")
    
    # Example SQLite to CSV download
    # sql_writer.sqlite_to_csv("Freedom(Future)", "freedom_export.csv")
