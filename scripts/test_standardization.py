import pandas as pd
import pytest

from scripts.standardization import (
    StandardSchema,
    BIMappingConfig,
    standardize_clickhouse_data,
    standardize_superset_data,
)


schema = StandardSchema()


def test_clickhouse_standardization_success():
    df = pd.DataFrame({
        "jour": ["2024-01-01"],
        "valeur": [100],
        "type": ["car"],
        "kpi": ["sales"]
    })

    mapping = BIMappingConfig(
        source_tool="clickhouse",
        mapping={
            "date": "jour",
            "value": "valeur",
            "category": "type",
            "kpi_title": "kpi"
        }
    )

    result = standardize_clickhouse_data(df, mapping, schema)

    assert list(result.columns) == schema.required_columns()
    assert result.iloc[0]["value"] == 100


def test_superset_table_response():
    superset_json = {
        "result": [
            {"ds": "2024-01-01", "val": 10, "cat": "A", "kpi": "sales"}
        ]
    }

    mapping = BIMappingConfig(
        source_tool="superset",
        mapping={
            "date": "ds",
            "value": "val",
            "category": "cat",
            "kpi_title": "kpi"
        }
    )

    df = standardize_superset_data(superset_json, mapping, schema)
    assert len(df) == 1


def test_superset_timeseries_response():
    superset_json = {
        "data": [
            {"ds": "2024-01-01", "value": 5, "category": "B", "kpi": "users"}
        ]
    }

    mapping = BIMappingConfig(
        source_tool="superset",
        mapping={
            "date": "ds",
            "value": "value",
            "category": "category",
            "kpi_title": "kpi"
        }
    )

    df = standardize_superset_data(superset_json, mapping, schema)
    assert df.iloc[0]["value"] == 5


def test_missing_columns_raises_error():
    df = pd.DataFrame({"a": [1]})

    mapping = BIMappingConfig(
        source_tool="clickhouse",
        mapping={
            "date": "jour",
            "value": "valeur",
            "category": "type",
            "kpi_title": "kpi"
        }
    )

    with pytest.raises(KeyError):
        standardize_clickhouse_data(df, mapping, schema)
