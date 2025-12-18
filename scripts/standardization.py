import logging
from dataclasses import dataclass
from typing import Dict, List, Any

import pandas as pd

# Logging Configuration
logger = logging.getLogger("bi_standardization")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# 1. Standard BI Schema


@dataclass(frozen=True)
class StandardSchema:
    date_col: str = "date"
    value_col: str = "value"
    category_col: str = "category"
    title_col: str = "kpi_title"

    def required_columns(self) -> List[str]:
        return [
            self.date_col,
            self.value_col,
            self.category_col,
            self.title_col,
        ]


# 2. Mapping Config

@dataclass(frozen=True)
class BIMappingConfig:
    source_tool: str
    mapping: Dict[str, str]  # standard_col -> source_col


# 3. Schema Validation
def validate_schema(
    df: pd.DataFrame,
    schema: StandardSchema
) -> None:
    """
    Ensures dataframe matches the expected BI schema.
    """
    missing = [col for col in schema.required_columns()
               if col not in df.columns]
    if missing:
        logger.error("Schema validation failed. Missing columns: %s", missing)
        raise ValueError(f"Missing required BI columns: {missing}")

    logger.info("Schema validation passed")


# 4. Shared Utilities

def _validate_and_rename(
    df: pd.DataFrame,
    mapping: Dict[str, str]
) -> pd.DataFrame:
    logger.info("Validating source columns")

    missing_cols = [src for src in mapping.values() if src not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing columns in source data: {missing_cols}")

    rename_dict = {src: std for std, src in mapping.items()}
    logger.info("Renaming columns: %s", rename_dict)

    return df.rename(columns=rename_dict)


def _apply_standard_types(
    df: pd.DataFrame,
    schema: StandardSchema
) -> pd.DataFrame:
    logger.info("Applying standard data types")

    df[schema.date_col] = pd.to_datetime(
        df[schema.date_col], errors="coerce"
    )
    df[schema.value_col] = pd.to_numeric(
        df[schema.value_col], errors="coerce"
    )

    for col in [schema.category_col, schema.title_col]:
        df[col] = df[col].astype("string")

    before = len(df)
    df = df.dropna(subset=[schema.date_col, schema.value_col])
    after = len(df)

    logger.info("Dropped %s invalid rows", before - after)

    return df


# 5. ClickHouse Standardization

def standardize_clickhouse_data(
    df: pd.DataFrame,
    mapping_config: BIMappingConfig,
    schema: StandardSchema
) -> pd.DataFrame:
    logger.info("Standardizing ClickHouse data")

    if df.empty:
        raise ValueError("ClickHouse input dataset is empty")

    df_std = _validate_and_rename(df, mapping_config.mapping)
    df_std = _apply_standard_types(df_std, schema)
    validate_schema(df_std, schema)

    return df_std


# 6. Superset Standardization (Variants)

def _extract_superset_rows(
    superset_json: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Handles Superset response variants:
    - table
    - timeseries
    - pivot
    """

    if "result" in superset_json:
        return superset_json["result"]

    if "data" in superset_json:
        # Timeseries or pivot
        data = superset_json["data"]

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            # Pivot-like structure
            rows = []
            for key, values in data.items():
                for item in values:
                    item["category"] = key
                    rows.append(item)
            return rows

    raise ValueError("Unsupported Superset response format")


def standardize_superset_data(
    superset_json: Dict[str, Any],
    mapping_config: BIMappingConfig,
    schema: StandardSchema
) -> pd.DataFrame:
    logger.info("Standardizing Superset data")

    rows = _extract_superset_rows(superset_json)
    if not rows:
        raise ValueError("Superset response contains no data")

    df = pd.DataFrame(rows)
    df_std = _validate_and_rename(df, mapping_config.mapping)
    df_std = _apply_standard_types(df_std, schema)
    validate_schema(df_std, schema)

    return df_std
