"""
Shared Spark utilities used by TelePulse processing pipelines.
"""

from pyspark.sql import SparkSession, DataFrame


def create_spark_session(app_name: str) -> SparkSession:
    """Create a Spark session with Hive support enabled."""

    return (
        SparkSession.builder
        .appName(app_name)
        .enableHiveSupport()
        .getOrCreate()
    )


def read_csv(
    spark: SparkSession,
    path: str,
    header: bool = True
) -> DataFrame:
    """Read one or more CSV files from HDFS."""

    return (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(path)
    )