"""
Transformation utilities shared by TelePulse processing pipelines.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def normalize_column_names(df: DataFrame) -> DataFrame:
    """Convert column names to lowercase."""

    renamed = df

    for column in df.columns:
        renamed = renamed.withColumnRenamed(
            column,
            column.lower()
        )

    return renamed


def cast_datetime_column(
    df: DataFrame,
    column_name: str = "datetime"
) -> DataFrame:
    """Cast the datetime column to BIGINT."""

    return df.withColumn(
        column_name,
        col(column_name).cast("long")
    )


def remove_duplicates(df: DataFrame) -> DataFrame:
    """Remove duplicate rows."""

    return df.dropDuplicates()

def transform_dataframe(
    df: DataFrame,
    datetime_column: str = "datetime",
) -> DataFrame:
    """Apply the standard TelePulse transformations."""

    df = normalize_column_names(df)
    df = cast_datetime_column(df, datetime_column)
    df = remove_duplicates(df)

    return df