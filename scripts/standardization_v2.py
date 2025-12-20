import pandas as pd
import numpy as np
import hashlib
from typing import List, Dict, Optional

class Standardizer:
    def __init__(self, target_columns: List[str], precision: int = 4):
        self.target_columns = sorted(target_columns)
        self.precision = precision

    def process(self, df: pd.DataFrame, source_mapping: Dict[str, str]) -> pd.DataFrame:
        """The 'Orchestrator' function that calls specific steps in order."""
        df = df.copy()
        
        # Step-by-step modular transformation
        df = df.rename(columns=source_mapping)
        df = self._align_schema(df)
        df = self._normalize_types(df)
        df = self._handle_nulls(df)
        df = self._add_signature(df)
        
        return df.sort_values(by='row_signature').reset_index(drop=True)

    # --- Private Helper Methods ---

    def _align_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensures the dataframe matches the target columns exactly."""
        for col in self.target_columns:
            if col not in df.columns:
                df[col] = np.nan
        return df[self.target_columns]

    def _normalize_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handles type casting for Dates, Strings, and Numbers."""
        for col in df.columns:
            # 1. Dates
            if 'time' in col.lower() or 'date' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # 2. Numerics
            elif pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].astype(float).round(self.precision)
            
            # 3. Strings
            elif pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].astype(str).str.strip().str.lower()
        return df

    def _handle_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Unified null representation to ensure hash consistency."""
        # Replace actual NaNs and common 'null' strings
        return df.fillna("null").replace(["none", "nan", "", "None"], "null")

    def _add_signature(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generates the cryptographic row signature."""
        # Sorting columns horizontally before hashing is a safety best practice
        df_sorted = df[sorted(df.columns)]
        df['row_signature'] = df_sorted.apply(self._generate_hash, axis=1)
        return df

    def _generate_hash(self, row: pd.Series) -> str:
        """Low-level string concatenation and hashing."""
        row_str = "|".join(row.astype(str).values)
        return hashlib.sha256(row_str.encode('utf-8')).hexdigest()