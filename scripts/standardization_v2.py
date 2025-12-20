import pandas as pd
import numpy as np
import hashlib

class Standardizer:
    def __init__(self, target_columns, precision=4):
        """
        :param target_columns: List of columns the final output MUST have.
        :param precision: Value for numerical columns rounding, 10^-4 by default
        """
        self.target_columns = sorted(target_columns)
        self.precision = precision

    def _generate_signature(self, row):
        """Creates a SHA256 hash of the row content."""
        # We concatenate all values in the row to create a unique fingerprint
        row_str = "".join(str(val) for val in row.values)
        return hashlib.sha256(row_str.encode()).hexdigest()

    def process(self, df, source_mapping):
        """
        :param df: The raw DataFrame (CH or SS)
        :param source_mapping: dict mapping raw source headers to target_columns
        """
        df = df.copy()

        # 1. Standardize Column Names (Schema Mapping)
        df = df.rename(columns=source_mapping)

        # 2. Align Columns (Union Schema)
        # Ensure only target columns exist. Add missing ones as NaN, drop extras.
        for col in self.target_columns:
            if col not in df.columns:
                df[col] = np.nan
        
        # Keep only the target columns to ensure signature consistency
        df = df[self.target_columns]

        # 3. Normalize Values
        for col in df.columns:
            # Normalize Strings
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip().str.lower()
            
            # Normalize Dates (Force YYYY-MM-DD for consistency)
            if 'time' in col or 'date' in col:
                df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Normalize Numeric Precision
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].astype(float).round(self.precision)
        # Handle Nulls consistently
        df = df.fillna("null").replace(["none", "nan", "", "nan", "None"], "null")

        # 4. Create a Deterministic Row Signature
        # Re-sorting columns here ensures the hash is identical even if sources vary
        df = df.reindex(sorted(df.columns), axis=1)
        df['row_signature'] = df.apply(self._generate_signature, axis=1)

        # 5. Sort by the Signature
        df = df.sort_values(by='row_signature').reset_index(drop=True)
        
        return df