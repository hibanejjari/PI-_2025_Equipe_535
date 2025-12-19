import sys
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from Clickhouse.fetch_clickhouse_data import ClickHouseManager
from scripts.standardization_v2 import Standardizer

# --- EXAMPLE USAGE ---

# Define how raw sources map to your "Standard" format
mapping_table = {
    "Time": "timestamp",
    "Value": "metric_value",
}

std = Standardizer(mapping_table)

# 1. Initialize the manager
ch_manager = ClickHouseManager(
    host='localhost', 
    port=8123, 
    user='default', 
    password='1234'
)

# 2. Define df_ch by fetching the table
# This uses the method we built in Step 2
df_ch = ch_manager.fetch_table("test_data")

print("\nClickHouse Data successfully loaded into df_ch.\n")
print(df_ch.head())

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SUPERSET_DATA = DATA_DIR /f"chart_120_data.csv"

df_ss = pd.read_csv(SUPERSET_DATA)

print("\nSuperset Data successfully loaded into df_ss.\n")
print(df_ss.head())

# Standardize both
clean_ch = std.process(df_ch)
clean_ss = std.process(df_ss)

print("\nStandardized with Signatures:")
print(clean_ch[['row_signature', 'timestamp', 'metric_value']].head())