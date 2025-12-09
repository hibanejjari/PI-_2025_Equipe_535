import pandas as pd
from dataclasses import dataclass
from typing import Dict


@dataclass
class StandardSchema:
    """
    Defines the target BI schema to standardize data.
    """
    date_col: str = "date"
    value_col: str = "value"
    category_col: str = "category"
    title_col: str = "kpi_title"


@dataclass
class BIMappingConfig:
    """
    Maps ClickHouse columns to the standard BI schema.
    Example:
        {
            "date": "jour",
            "value": "valeur",
            "category": "type_vehicule",
            "kpi_title": "kpi"
        }
    """
    source_tool: str
    mapping: Dict[str, str]


def standardize_clickhouse_data(
    df: pd.DataFrame,
    mapping_config: BIMappingConfig,
    standard_schema: StandardSchema
) -> pd.DataFrame:
    """
    Standardizes raw ClickHouse data into a unified BI format.

    Steps:
        1. Validate dataframe not empty
        2. Check required mapping columns exist
        3. Rename columns using mapping
        4. Convert types (date → datetime, value → float, others → string)
        5. Drop invalid rows (NaT or NaN)
        6. Return standardized dataframe
    """

    # 1 — Check empty input
    if df.empty:
        raise ValueError("ClickHouse input dataset is empty.")

    # 2 — Validate that all source columns exist
    missing_cols = [
        src for src in mapping_config.mapping.values() if src not in df.columns
    ]
    if missing_cols:
        raise KeyError(f"Missing columns in ClickHouse data: {missing_cols}")

    # 3 — Rename columns to the standard schema
    rename_dict = {src: std for std, src in mapping_config.mapping.items()}
    df_std = df.rename(columns=rename_dict)

    # 4 — Type conversions
    # Convert date
    if standard_schema.date_col in df_std:
        df_std[standard_schema.date_col] = pd.to_datetime(
            df_std[standard_schema.date_col], errors="coerce"
        )

    # Convert numeric value
    if standard_schema.value_col in df_std:
        df_std[standard_schema.value_col] = pd.to_numeric(
            df_std[standard_schema.value_col], errors="coerce"
        )

    # Convert category + title to string
    for col in [standard_schema.category_col, standard_schema.title_col]:
        if col in df_std:
            df_std[col] = df_std[col].astype("string")

    # 5 — Remove invalid rows
    df_std = df_std.dropna(subset=[standard_schema.date_col, standard_schema.value_col])

    return df_std
