from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum,
    hour,
    when,
    log,
    from_unixtime,
    to_timestamp
)

HDFS_ROOT = "hdfs://master:8020/telepulse"


def create_spark_session():
    """Initializes and returns a Spark session with Hive support."""
    return (
        SparkSession.builder
        .appName("TelePulse_Analytics_Pipeline")
        .enableHiveSupport()
        .getOrCreate()
    )


# Reads the merged telecommunication datasets from HDFS.
def load_data(spark):

    base_path = f"{HDFS_ROOT}/merged/"

    # Read activity dataset
    df_activity = spark.read.csv(
        f"{base_path}sms_call_internet_all.csv",
        header=True,
        inferSchema=True
    ).fillna(0)

    # Convert datetime string to timestamp
    df_activity = df_activity.withColumn(
        "datetime",
        to_timestamp(col("datetime"))
    )

    # Read province interaction dataset
    df_provinces = spark.read.csv(
        f"{base_path}mi_to_provinces_all.csv",
        header=True,
        inferSchema=True
    ).fillna(0)

    return df_activity, df_provinces


# Calculates overall Activity Density per grid square.
def calculate_urban_vitality(df_activity):

    print("Calculating Urban Vitality Index...")

    vitality_df = (
        df_activity
        .groupBy("CellID")
        .agg(
            sum("smsin").alias("total_sms_in"),
            sum("smsout").alias("total_sms_out"),
            sum("callin").alias("total_call_in"),
            sum("callout").alias("total_call_out"),
            sum("internet").alias("total_internet")
        )
        .withColumn(
            "urban_vitality_index",
            col("total_sms_in")
            + col("total_sms_out")
            + col("total_call_in")
            + col("total_call_out")
            + col("total_internet")
        )
    )

    vitality_df.write.mode("overwrite").saveAsTable("telepulse.urban_vitality")

    return vitality_df


# Classifies Land Use based on peak activity hours.
def classify_land_use(df_activity):

    print("Classifying Land Use Zones...")

    # Extract hour from timestamp
    df_with_hour = df_activity.withColumn(
        "hour",
        hour(col("datetime"))
    )

    # Separate activity into Business Hours (9-17) and Residential Hours
    land_use_df = (
        df_with_hour
        .withColumn(
            "business_activity",
            when(
                (col("hour") >= 9) & (col("hour") <= 17),
                col("internet") + col("callin")
            ).otherwise(0)
        )
        .withColumn(
            "residential_activity",
            when(
                (col("hour") < 9) | (col("hour") > 17),
                col("internet") + col("callin")
            ).otherwise(0)
        )
    )

    classified_df = (
        land_use_df
        .groupBy("CellID")
        .agg(
            sum("business_activity").alias("total_business"),
            sum("residential_activity").alias("total_residential")
        )
        .withColumn(
            "land_use_category",
            when(
                col("total_business") > col("total_residential"),
                "Business/Office"
            ).otherwise("Residential")
        )
    )

    classified_df.write.mode("overwrite").saveAsTable(
        "telepulse.land_use_classification"
    )

    return classified_df


# Calculates Spatial Diversity Index (Shannon Entropy) based on directional interaction strengths.
def calculate_spatial_diversity(df_provinces):

    print("Calculating Spatial Diversity Index (Shannon Entropy)...")

    total_inter_df = (
        df_provinces
        .groupBy("CellID")
        .agg(
            sum("cell2Province").alias("total_interactions")
        )
    )

    df_prob = (
        df_provinces
        .join(total_inter_df, "CellID")
        .withColumn(
            "p_ia",
            col("cell2Province") / col("total_interactions")
        )
    )

    entropy_df = (
        df_prob
        .withColumn(
            "entropy_calc",
            -1 * col("p_ia") * log(col("p_ia"))
        )
        .groupBy("CellID")
        .agg(
            sum("entropy_calc").alias(
                "shannon_entropy_diversity_index"
            )
        )
    )

    entropy_df.write.mode("overwrite").saveAsTable(
    "telepulse.spatial_diversity"
    )

    return entropy_df


def main():

    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    spark.sql("DROP DATABASE IF EXISTS telepulse CASCADE")
    spark.sql("CREATE DATABASE telepulse")
    spark.catalog.setCurrentDatabase("telepulse")

    try:

        df_activity, df_provinces = load_data(spark)

        calculate_urban_vitality(df_activity)
        classify_land_use(df_activity)
        calculate_spatial_diversity(df_provinces)

        print("SUCCESS: All TelePulse Analytics Jobs Completed and Saved to Hive!")

    except Exception as e:
        print(f"An error occurred during execution: {e}")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()