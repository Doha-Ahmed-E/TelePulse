"""
Hive utilities shared by TelePulse processing pipelines.
"""

from pathlib import Path
from pyspark.sql import DataFrame, SparkSession
from .constants import DATABASE_NAME


def execute_sql_file(
    spark: SparkSession,
    sql_file: Path,
) -> None:
    """
    Execute all SQL statements contained in a .hql file.
    """

    sql_path = Path(sql_file)

    with sql_path.open("r", encoding="utf-8") as file:
        script = file.read()

    for statement in script.split(";"):
        statement = statement.strip()

        if statement:
            spark.sql(statement)


def overwrite_table(
    df: DataFrame,
    table_name: str,
) -> None:
    """
    Replace the contents of an existing Hive table.
    """

    (
        df.write
        .mode("overwrite")
        .insertInto(
            f"{DATABASE_NAME}.{table_name}",
            overwrite=True,
        )
    )


def append_table(
    df: DataFrame,
    table_name: str,
) -> None:
    """
    Append rows to an existing Hive table.
    """

    (
        df.write
        .mode("append")
        .insertInto(
            f"{DATABASE_NAME}.{table_name}",
        )
    )