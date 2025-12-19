import clickhouse_connect
import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
HOST = 'localhost'
PORT = 8123
USER = 'default'
PASSWORD = '1234'

PROJECT_ROOT = Path(__file__).parent.parent
# Path of the folder 'data'
DATA_DIR = PROJECT_ROOT / "data"

DATA_PATH = DATA_DIR / "test_reference_data.csv"

class ClickHouseManager:
    def __init__(self, host=HOST, port=PORT, user=USER, password=PASSWORD):
        self.client = clickhouse_connect.get_client(host=host, port=port, username=user, password=password)

    def _map_dtype(self, col_name, dtype):
        """Maps Pandas dtypes to ClickHouse dtypes."""
        str_dtype = str(dtype)
        if 'int' in str_dtype:
            return 'Int64'
        elif 'float' in str_dtype:
            return 'Float64'
        elif 'datetime' in str_dtype:
            return 'DateTime'
        else:
            return 'String'

    def import_csv(self, file_path, table_name):
        # 1. Read data and attempt to parse dates
        df = pd.read_csv(file_path, parse_dates=True)
        
        # Ensure 'Time' or date columns are actual datetime objects for ClickHouse
        for col in df.columns:
            if 'time' in col.lower() or 'date' in col.lower():
                df[col] = pd.to_datetime(df[col])

        # 2. Build the Column Definitions
        cols_definition = ", ".join([
                f"`{col}` {self._map_dtype(col, df[col].dtype)}" 
                for col in df.columns
            ])
        
        # 3. Create Table (using first column as the Order By key)
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {cols_definition}
        ) ENGINE = MergeTree() 
        ORDER BY `{df.columns[0]}`
        """
        
        print(f"Executing: {create_query}")
        self.client.command(f"DROP TABLE IF EXISTS {table_name}")
        self.client.command(create_query)

        # 4. Insert Data
        self.client.insert(table_name, df)
        print(f"Successfully imported {len(df)} rows into '{table_name}' automatically.")  

    def import_excel(self, file_path, table_name):
        # 1. Read data and attempt to parse dates
        df = pd.read_excel(file_path, parse_dates=True)
        
        # Ensure 'Time' or date columns are actual datetime objects for ClickHouse
        for col in df.columns:
            if 'time' in col.lower() or 'date' in col.lower():
                df[col] = pd.to_datetime(df[col])

        # 2. Build the Column Definitions
        cols_definition = ", ".join([
                f"`{col}` {self._map_dtype(col, df[col].dtype)}" 
                for col in df.columns
            ])
        
        # 3. Create Table (using first column as the Order By key)
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {cols_definition}
        ) ENGINE = MergeTree() 
        ORDER BY `{df.columns[0]}`
        """
        
        print(f"Executing: {create_query}")
        self.client.command(f"DROP TABLE IF EXISTS {table_name}")
        self.client.command(create_query)

        # 4. Insert Data
        self.client.insert(table_name, df)
        print(f"Successfully imported {len(df)} rows into '{table_name}' automatically.")        

    def fetch_table(self, table_name):
        """Fetches an entire table from ClickHouse and returns a Pandas DataFrame."""
        print(f"Fetching data from table: {table_name}...")
        
        # .query_df handles the conversion from ClickHouse blocks to Pandas automatically
        df = self.client.query_df(f"SELECT * FROM {table_name}")
        
        return df

if __name__ == "__main__":
    Clickhouse = ClickHouseManager()
    
    # Use import_csv for CSV data and import_excel for Excel data
    Clickhouse.import_csv(DATA_PATH, "test_data")
    #Clickhouse.import_excel(DATA_PATH, "test_data")

# 2. Fetch the data back
    ch_data = Clickhouse.fetch_table("test_data")
    
    # 3. Preview the fetched data
    print("\n--- Fetched Data Preview ---")
    print(ch_data.head())
    print("\nData Types:")
    print(ch_data.dtypes)