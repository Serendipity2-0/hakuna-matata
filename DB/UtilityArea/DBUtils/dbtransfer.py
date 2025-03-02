import sqlite3

def transfer_tables(source_db, target_db):
    """
    Transfers all tables and their data from a source SQLite database to a target SQLite database.
    
    Args:
        source_db (str): Path to the source SQLite database file
        target_db (str): Path to the target SQLite database file
        
    The function performs the following steps:
    1. Connects to both source and target databases
    2. Retrieves list of tables from source database
    3. For each table:
        - Fetches all rows and column information
        - Creates the table in target database if it doesn't exist
        - Copies all data from source to target
    4. Commits changes and closes connections
    """
    print(f"Connecting to source database: {source_db}")
    source_conn = sqlite3.connect(source_db)
    print(f"Connecting to target database: {target_db}")
    target_conn = sqlite3.connect(target_db)
    
    print("Fetching list of tables from the source database...")
    source_cursor = source_conn.cursor()
    source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = source_cursor.fetchall()
    print(f"Tables found: {[table[0] for table in tables]}")
    
    for table_name in tables:
        table = table_name[0]
        if table == 'sqlite_sequence':
            print("Skipping sqlite_sequence table (internal SQLite table)")
            continue
            
        print(f"Processing table: {table}")
        source_cursor.execute(f'SELECT * FROM "{table}"')
        rows = source_cursor.fetchall()
        print(f"Number of rows fetched from {table}: {len(rows)}")
        
        columns = [description[0] for description in source_cursor.description]
        column_str = ', '.join(columns)
        print(f"Columns in {table}: {column_str}")
        
        target_cursor = target_conn.cursor()
        target_cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({column_str})')
        print(f"Table {table} created in target database if it did not exist.")
        
        for row in rows:
            placeholders = ', '.join('?' * len(row))
            target_cursor.execute(f'INSERT INTO "{table}" VALUES ({placeholders})', row)
        print(f"Inserted {len(rows)} rows into {table} in target database.")
    
    print("Committing changes to target database...")
    target_conn.commit()
    print("Closing source database connection...")
    source_conn.close()
    print("Closing target database connection...")
    target_conn.close()

# Call the function to transfer tables
transfer_tables('backend/databases/kaas.db', 'backend/databases/kaas_ref.db')
