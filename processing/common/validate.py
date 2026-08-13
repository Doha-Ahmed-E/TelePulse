"""
Validation utilities shared by TelePulse processing pipelines.
"""

from pyspark.sql import DataFrame


def validate_columns(df: DataFrame, expected_columns: list[str]) -> None:
    """Ensure the DataFrame contains the expected columns."""

    actual = set(df.columns)
    expected = set(expected_columns)

    missing = expected - actual
    unexpected = actual - expected

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    if unexpected:
        raise ValueError(
            f"Unexpected columns: {sorted(unexpected)}"
        )


def validate_not_empty(df: DataFrame, dataset_name: str) -> None:
    """Ensure the DataFrame contains data."""

    if df.rdd.isEmpty():
        raise ValueError(
            f"{dataset_name} dataset is empty."
        )

def validate_dataframe(
    df: DataFrame,
    expected_columns: list[str],
    dataset_label: str,
) -> None:
    """Validate a DataFrame."""

    validate_columns(
        df,
        expected_columns,
    )

    validate_not_empty(
        df,
        dataset_label,
    )