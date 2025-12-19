## Key functions:

1. **Read**: Opens a local CSV or Excel file.

2. **Analyze**: Automatically detects data types (Int, Float, Date, or String).

3. **Schema Creation**: Dynamically generates a CREATE TABLE SQL query.

4. **Load**: Injects the data into ClickHouse.

5. **Verify**: Pulls the data back into Python to confirm success.

## 🔑 Key Components
1. **Configuration & Pathing**

    - Database Credentials: Connects to a local ClickHouse instance (port 8123) using a default password (1234).

    - Dynamic Paths: Uses pathlib to ensure the script finds the /data folder regardless of the operating system or where the script is launched from.

2. **The ClickHouseManager Class**

This is the "brain" of the script. It contains three main capabilities:

    - _map_dtype: A helper function that translates Python/Pandas data types into ClickHouse-specific SQL types (e.g., datetime64 becomes DateTime).

    - import_csv / import_excel:

        - Cleans date columns automatically.

        - Generates the CREATE TABLE statement with backticks (`) to handle spaces or special characters in column names.

        - Uses the MergeTree engine (ClickHouse's primary high-performance engine).

    - fetch_table: Uses query_df to return data from the database directly as a Pandas DataFrame for immediate use in Python.

3. **Execution Logic** (if __name__ == "__main__":)

    - Automation: When run directly, it initializes the manager, wipes the old table, imports the new data, and prints a preview of the results.

    - Validation: It finishes by displaying the data types fetched from the database, allowing you to verify that the "Standardization" worked (e.g., confirming dates are no longer just strings).