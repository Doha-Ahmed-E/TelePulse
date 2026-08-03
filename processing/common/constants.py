"""
Shared constants used by TelePulse processing pipelines.
"""

# Hive

DATABASE_NAME = "telepulse"

SMS_TABLE = "sms_call_internet"

PROVINCE_TABLE = "cell_provinces"


# HDFS

ARCHIVE_ROOT = "/telepulse/archive"

SMS_ARCHIVE_PATH = (
    f"{ARCHIVE_ROOT}/sms-call-internet-mi-2013-11-*.csv"
)

PROVINCE_ARCHIVE_PATH = (
    f"{ARCHIVE_ROOT}/mi-to-provinces-2013-11-*.csv"
)


# Spark

BOOTSTRAP_APP_NAME = "TelePulse Bootstrap"

INGESTION_APP_NAME = "TelePulse Ingestion"