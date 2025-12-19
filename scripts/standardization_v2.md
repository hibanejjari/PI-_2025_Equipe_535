## Key functions

1. **Semantic Mapping**: Uses a provided dictionary to rename source-specific headers (e.g., SUM(New Members)) into standardized internal names (e.g., metric_value).

2. **Schema Enforcement**: Strictly aligns the DataFrame to a "Target Schema." It discards irrelevant metadata columns and injects NaN for missing columns, ensuring both datasets have the exact same shape.

3. **Multi-Type Normalization**: * Strings: Strips whitespace and forces lowercase to avoid "hidden" mismatches.

    - Dates: Converts all timestamps into a standardized string format (YYYY-MM-DD HH:MM:SS) to bypass varied database time-storage formats.

    - Numeric: Rounds floats to 4 decimal places to prevent false-negative comparisons caused by floating-point math errors.

4. **Null Standardization**: Replaces all variations of empty data (None, NaN, "", "nan") with a single string literal "null" for consistent hashing.

5. **Deterministic Fingerprinting (Hashing)**: Concatenates all row values and passes them through a SHA256 hash function. This creates a row_signature—a unique string that represents that specific row's content.

6. **Positional Independence**: Finally, it sorts the entire dataset by the row_signature. This means the original order of the data (from the database or CSV) no longer matters; identical datasets will always result in the same physical row order.