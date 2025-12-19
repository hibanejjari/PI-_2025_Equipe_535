import pandas as pd
import numpy as np
import hashlib

class Standardizer:
    def __init__(self, schema_mapping):
        """
        :param schema_mapping: dict { 'raw_column_name': 'canonical_name' }
        """
        self.mapping = schema_mapping

    def _generate_signature(self, row):
        """Creates a SHA256 hash of the row content."""
        # We concatenate all values as strings to create a unique fingerprint
        row_str = "".join(str(val) for val in row.values)
        return hashlib.sha256(row_str.encode()).hexdigest()

    def process(self, df):
        df = df.copy()

        # 1. Standardize Column Names (Schema Mapping)
        df = df.rename(columns=self.mapping)

        # 2. Align Columns (Union Schema)
        # Ensure all mapped columns exist; if missing, fill with NaN
        for col in set(self.mapping.values()):
            if col not in df.columns:
                df[col] = np.nan

        # 3. Normalize Values (Critical)
        for col in df.columns:
            # Normalize Strings
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip().str.lower()
            
            # Normalize Dates
            if 'time' in col or 'date' in col:
                df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Normalize Numeric Precision
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].astype(float).round(4)

        # Handle Nulls consistently (replace all variations with "null")
        df = df.fillna("null").replace(["none", "nan", ""], "null")

        # 4. Create a Deterministic Row Signature
        # We apply this to a sorted version of the columns to ensure consistency
        df = df.reindex(sorted(df.columns), axis=1)
        df['row_signature'] = df.apply(self._generate_signature, axis=1)

        # 5. Sort by the Signature
        df = df.sort_values(by='row_signature').reset_index(drop=True)
        
        return df