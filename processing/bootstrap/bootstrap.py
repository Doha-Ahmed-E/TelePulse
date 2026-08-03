"""
Bootstrap the TelePulse warehouse from the historical archive.
"""

from pathlib import Path
from processing.common.constants import (
    BOOTSTRAP_APP_NAME,
    PROVINCE_ARCHIVE_PATH,
    PROVINCE_TABLE,
    SMS_ARCHIVE_PATH,
    SMS_TABLE,
)
from processing.common.hive import (
    execute_sql_file,
    overwrite_table,
)
from processing.common.schema import (
    PROVINCE_COLUMNS,
    SMS_COLUMNS,
)
from processing.common.utils import (
    create_spark_session,
    read_csv,
)
from processing.common.validate import (validate_dataframe) 
from processing.common.transform import (transform_dataframe)


ROOT = Path(__file__).resolve().parents[2]

CREATE_TABLES_SQL = ROOT / "processing" / "hive" / "create_tables.hql"
CREATE_ANALYTICS_SQL = ROOT / "processing" / "hive" / "create_analytics.hql"


def main() -> None:

    spark = create_spark_session(BOOTSTRAP_APP_NAME)

    try:   

        # Read historical datasets
        sms_df = read_csv(
            spark,
            SMS_ARCHIVE_PATH,
        )
        province_df = read_csv(
            spark,
            PROVINCE_ARCHIVE_PATH,
        )

        # Validate source data
        validate_dataframe(
            sms_df,
            SMS_COLUMNS,
            "SMS",
        )
        validate_dataframe(
            province_df,
            PROVINCE_COLUMNS,
            "Province",
        )

        # Transform datasets
        sms_df = transform_dataframe(sms_df)
        province_df = transform_dataframe(province_df)

        # Initialize warehouse
        execute_sql_file(
            spark,
            CREATE_TABLES_SQL,
        )

        # Load warehouse tables
        overwrite_table(
            sms_df,
            SMS_TABLE,
        )
        overwrite_table(
            province_df,
            PROVINCE_TABLE,
        )

        # Create analytics views      
        execute_sql_file(
            spark,
            CREATE_ANALYTICS_SQL,
        )

        print("TelePulse warehouse initialized successfully.")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()